"""Local web app: upload a PPTX, get a narrated video back.

Run:  ./run.sh   (serves http://127.0.0.1:8765, local machine only)
The ElevenLabs (and optional OpenAI/Anthropic) API keys are held in memory for the running job only; it is never written to disk.
"""
import json
import os
import shutil
import threading
import traceback
import uuid
from pathlib import Path

from flask import Flask, abort, jsonify, request, send_file, send_from_directory

import pipeline
import tagging

ROOT = Path(__file__).resolve().parent
# Packaged builds point this at a user-writable folder (see launcher.py).
DATA = Path(os.environ.get('SLIDE2VIDEO_DATA') or ROOT / 'data')
JOBS = DATA / 'jobs'
CACHE = DATA / 'tts-cache'
JOBS.mkdir(parents=True, exist_ok=True)

app = Flask(__name__, static_folder=None)
app.config['MAX_CONTENT_LENGTH'] = 300 * 1024 * 1024
jobs = {}
lock = threading.Lock()


def public(job):
    return {k: v for k, v in job.items() if not k.startswith('_')}


def load_jobs():
    """Pick up decks uploaded in earlier runs so cached work isn't lost on restart."""
    for d in JOBS.iterdir():
        meta = d / 'job.json'
        if meta.exists():
            job = json.loads(meta.read_text())
            if job['status'] == 'running':
                job.update(status='error', error='Sunucu yeniden başlatıldığı için yarıda kaldı. Yeniden başlatın; tamamlanan seslendirmeler tekrar kullanılır.')
            jobs[job['id']] = job


def save(job):
    (JOBS / job['id'] / 'job.json').write_text(json.dumps(public(job), ensure_ascii=False, indent=1))


@app.get('/')
def index():
    return send_from_directory(ROOT / 'static', 'index.html')


def clear_pages(d):
    """Drop exported/rendered slide images so the next run uses the current PDF source."""
    (d / 'slides.pdf').unlink(missing_ok=True)
    for pages in d.glob('pages-*'):
        shutil.rmtree(pages, ignore_errors=True)


def attach_pdf(job, f):
    """Store an uploaded PDF as the job's slide images (instead of exporting the .pptx)."""
    if not f.filename.lower().endswith('.pdf'):
        raise pipeline.PipelineError('Lütfen bir .pdf dosyası seçin.')
    d = JOBS / job['id']
    tmp = d / 'uploaded.part.pdf'
    f.save(tmp)
    try:
        pipeline.check_pdf(tmp, job['slides'])
    except pipeline.PipelineError:
        tmp.unlink(missing_ok=True)
        raise
    tmp.replace(d / 'uploaded.pdf')
    clear_pages(d)
    job['pdf'] = f.filename


@app.post('/api/upload')
def upload():
    f = request.files.get('deck')
    if not f or not f.filename.lower().endswith('.pptx'):
        return jsonify(error='Lütfen bir .pptx dosyası yükleyin (konuşmacı notları seslendirme metni olur).'), 400
    job_id = uuid.uuid4().hex[:12]
    d = JOBS / job_id
    d.mkdir()
    path = d / 'deck.pptx'
    f.save(path)
    try:
        slides = pipeline.read_deck(path)
    except Exception as e:
        shutil.rmtree(d, ignore_errors=True)
        return jsonify(error=f'Sunum okunamadı: {e}'), 400
    job = {'id': job_id, 'name': f.filename, 'status': 'ready', 'stage': '', 'progress': 0, 'log': [],
           'slides': slides, 'result': None, 'error': None, 'pdf': None}
    if request.files.get('pdf'):
        try:
            attach_pdf(job, request.files['pdf'])
        except pipeline.PipelineError as e:
            shutil.rmtree(d, ignore_errors=True)
            return jsonify(error=str(e)), 400
    with lock:
        jobs[job_id] = job
    save(job)
    return jsonify(public(job))


@app.post('/api/jobs/<job_id>/pdf')
def add_pdf(job_id):
    job = jobs.get(job_id) or abort(404)
    if job['status'] == 'running':
        return jsonify(error='Önce işlemin bitmesini bekleyin.'), 409
    f = request.files.get('pdf')
    if not f:
        return jsonify(error='PDF dosyası gelmedi.'), 400
    try:
        attach_pdf(job, f)
    except pipeline.PipelineError as e:
        return jsonify(error=str(e)), 400
    save(job)
    return jsonify(public(job))


@app.delete('/api/jobs/<job_id>/pdf')
def remove_pdf(job_id):
    job = jobs.get(job_id) or abort(404)
    if job['status'] == 'running':
        return jsonify(error='Önce işlemin bitmesini bekleyin.'), 409
    (JOBS / job_id / 'uploaded.pdf').unlink(missing_ok=True)
    clear_pages(JOBS / job_id)
    job['pdf'] = None
    save(job)
    return jsonify(public(job))


@app.get('/api/jobs/<job_id>')
def status(job_id):
    job = jobs.get(job_id) or abort(404)
    return jsonify(public(job))


@app.post('/api/jobs/<job_id>/start')
def start(job_id):
    job = jobs.get(job_id) or abort(404)
    if job['status'] == 'running':
        return jsonify(error='Bu sunum zaten işleniyor.'), 409
    body = request.get_json(force=True)
    key = (body.get('api_key') or '').strip()
    if not key and not pipeline.FAKE_TTS:
        return jsonify(error='ElevenLabs API anahtarınızı girin.'), 400
    try:
        speed = float(body.get('speed', 1))
    except ValueError:
        return jsonify(error='Geçersiz hız.'), 400
    if not 0.5 <= speed <= 2.5:
        return jsonify(error='Hız 0,5× ile 2,5× arasında olmalı.'), 400
    if body.get('resolution') not in pipeline.RESOLUTIONS:
        return jsonify(error='Bilinmeyen çözünürlük.'), 400
    if body.get('transition', 'cut') not in ('cut', 'fade'):
        return jsonify(error='Bilinmeyen slayt geçişi.'), 400
    narrations = body.get('narrations') if body.get('auto_tags') else None
    if narrations is not None and not isinstance(narrations, dict):
        return jsonify(error='Geçersiz seslendirme metni.'), 400
    opts = {'api_key': key, 'auto_tags': bool(body.get('auto_tags')), 'narrations': narrations,
            'llm_key': (body.get('llm_key') or '').strip(),
            'voice_id': (body.get('voice_id') or pipeline.DEFAULT_VOICE).strip(),
            'model': (body.get('model') or pipeline.DEFAULT_MODEL).strip(),
            'language': (body.get('language') or '').strip(),
            'speed': speed, 'resolution': body['resolution'], 'transition': body.get('transition', 'cut'),
            'original_name': job['name']}
    job.update(status='running', stage='Başlatılıyor', progress=0, log=[], result=None, error=None,
               settings={k: v for k, v in opts.items() if k not in ('api_key', 'llm_key', 'narrations')})
    if narrations:
        job['narrations'] = narrations
    save(job)

    def report(stage, progress, message):
        job.update(stage=stage, progress=round(progress, 3))
        job['log'].append(message)

    def work():
        try:
            job['result'] = pipeline.run(JOBS / job_id, JOBS / job_id / 'deck.pptx', opts, CACHE, report)
            job.update(status='done', stage='Tamamlandı', progress=1)
        except pipeline.PipelineError as e:
            job.update(status='error', error=str(e))
        except Exception as e:
            traceback.print_exc()
            job.update(status='error', error=f'{type(e).__name__}: {e}')
        save(job)

    threading.Thread(target=work, daemon=True).start()
    return jsonify(public(job))


@app.post('/api/jobs/<job_id>/tags')
def tags(job_id):
    """Preview: tag the notes (model if an OpenAI/Anthropic key is given, rules otherwise)."""
    job = jobs.get(job_id) or abort(404)
    body = request.get_json(force=True)
    visible = [s for s in job['slides'] if not s['hidden']]
    try:
        narrations, info = tagging.tag_notes(visible, body.get('llm_key', ''))
    except pipeline.PipelineError as e:
        return jsonify(error=str(e)), 400
    except Exception as e:
        traceback.print_exc()
        return jsonify(error=f'Etiketler oluşturulamadı: {type(e).__name__}: {e}'), 500
    job['narrations'] = {str(k): v for k, v in narrations.items()}
    save(job)
    return jsonify(narrations=job['narrations'], info=info, summary=pipeline.tag_summary(info))


@app.get('/api/jobs/<job_id>/video')
def video(job_id):
    job = jobs.get(job_id) or abort(404)
    if job['status'] != 'done':
        abort(404)
    path = JOBS / job_id / job['result']['file']
    return send_file(path, as_attachment=request.args.get('download') == '1',
                     download_name=job['result']['file'], conditional=True)


@app.delete('/api/jobs/<job_id>')
def delete(job_id):
    job = jobs.get(job_id) or abort(404)
    if job['status'] == 'running':
        return jsonify(error='Önce işlemin bitmesini bekleyin.'), 409
    shutil.rmtree(JOBS / job_id, ignore_errors=True)
    jobs.pop(job_id, None)
    return jsonify(ok=True)


def _key():
    key = request.headers.get('X-Api-Key', '').strip()
    if not key:
        abort(400)
    return key


@app.get('/api/voices')
def voices():
    try:
        return jsonify(voices=pipeline.list_voices(_key()))
    except pipeline.PipelineError as e:
        return jsonify(error=str(e)), 400


@app.get('/api/account')
def account():
    try:
        return jsonify(pipeline.subscription(_key()))
    except pipeline.PipelineError as e:
        return jsonify(error=str(e)), 400


def renderer_name():
    try:
        return pipeline.RENDERER_NAMES.get(pipeline.renderer(required=False))
    except pipeline.PipelineError:
        return None


@app.get('/api/config')
def config():
    return jsonify(default_voice=pipeline.DEFAULT_VOICE, default_model=pipeline.DEFAULT_MODEL,
                   resolutions=list(pipeline.RESOLUTIONS), fake_tts=pipeline.FAKE_TTS,
                   renderer=renderer_name(),
                   free_mb=shutil.disk_usage(DATA).free // 2**20)


if __name__ == '__main__':
    load_jobs()
    app.run(host='127.0.0.1', port=8765, threaded=True)
