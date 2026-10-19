"""Expressive ElevenLabs audio tags ([short pause], [calmly], [inhales] ...) for speaker notes.

With an Anthropic or OpenAI key a model places the tags; without one a small rule set does.
Either way the note text itself never changes: only tags are inserted, and any model output whose
words differ from the original note is discarded in favour of the rules.
"""
import concurrent.futures
import os
import re

from pipeline import PipelineError

CLAUDE_MODEL = 'claude-opus-5-5'
OPENAI_MODELS = [m for m in (os.environ.get('SLIDE2VIDEO_OPENAI_MODEL'), 'gpt-5.6', 'gpt-5.5') if m]

ALLOWED = {'short pause', 'long pause', 'slowly', 'calmly', 'warmly', 'curious', 'thoughtful', 'serious',
           'reassuring', 'inhales', 'exhales', 'sighs', 'clears throat'}
TAG = re.compile(r'\[([^\[\]]{1,40})\]')

SYSTEM = """You prepare Turkish narration for a corporate training video that will be voiced by ElevenLabs (eleven_v3/eleven_v4), which understands audio tags in square brackets.

Insert audio tags into the narration so it sounds like a calm, natural human presenter. Allowed tags, all in English and lowercase:
[short pause] [long pause] [slowly] [calmly] [warmly] [curious] [thoughtful] [serious] [reassuring] [inhales] [exhales] [sighs] [clears throat]

Guidelines:
- Use tags sparingly: roughly one tag every two or three sentences. Put a tag directly before the words it affects.
- [short pause] before list items, after lead-ins that end with a colon, and before an important conclusion.
- [slowly] or [serious] before a key rule or warning; [calmly] or [reassuring] before practical advice; [curious] or [thoughtful] before a rhetorical question.
- [warmly] for a greeting at the very start of the video and for the closing thanks.
- Breath and voice sounds ([inhales], [exhales], [sighs], [clears throat]) at most once per slide, only where a real speaker would naturally make them, for example [inhales] before starting a long new section.

Return only the narration with the tags inserted. Do not change, add, remove, translate or reorder any of the original words or punctuation. No comments, quotes or markdown."""


def provider(key):
    return 'anthropic' if key.startswith('sk-ant-') else 'openai'


def strip_tags(text):
    return ' '.join(TAG.sub(' ', text).split())


def has_tags(text):
    return bool(TAG.search(text))


def _clean(text, original):
    """Keep only allowed tags; None if the words differ from the original note."""
    text = TAG.sub(lambda m: m.group(0) if m.group(1).strip().lower() in ALLOWED else ' ', text.strip())
    text = ' '.join(text.split())
    return text if strip_tags(text) == strip_tags(original) else None


# ---------------------------------------------------------------- rules

_SENT = re.compile(r'(?<=[.!?:;])\s+')
_ORDINAL = re.compile(r'^((birincisi|ikincisi|üçüncüsü|dördüncüsü|beşincisi|altıncısı|yedincisi|sekizincisi|'
                      r'dokuzuncusu|onuncusu|ilk olarak|son olarak|öncelikle|ilk durakta|son durakta)\b'
                      r'|(bir|iki|üç|dört|beş|altı|yedi|sekiz|dokuz|on|\d+)[.:)])', re.I)
_TURN = re.compile(r'^(örneğin|ancak|fakat|ama|ayrıca|ardından|öte yandan)\b', re.I)
_KEY = re.compile(r'(unutmayın|önemli|temel kural|kesinlikle|mutlaka|asla|hiçbir zaman|dikkat|şudur|'
                  r'yasak|zorunlu)', re.I)
_CALM = re.compile(r'^(emin değilseniz|endişelenmeyin|lütfen|böyle bir durumda|bu durumda|'
                   r'tereddüt ederseniz|merak etmeyin|şüphe)', re.I)
_WARM_END = re.compile(r'(teşekkür|sorularınız|iyi çalışmalar|görüşmek üzere|katılımınız)', re.I)
_WARM_START = re.compile(r'^(merhaba|hoş geldiniz|herkese merhaba|değerli)', re.I)


def _lower(s):
    return s.replace('İ', 'i').replace('I', 'ı').lower()


def rule_tags(text, first=False, last=False):
    """A few conservative cues, in the spirit of the hand-tagged KVKK narration."""
    sentences = [s for s in _SENT.split(' '.join(text.split())) if s]
    out, since = [], 9
    for i, s in enumerate(sentences):
        low = _lower(s)
        prev = sentences[i - 1] if i else ''
        tag = None
        if i == 0 and (first or _WARM_START.match(low)):
            tag = '[warmly]'
        elif last and i == len(sentences) - 1 and _WARM_END.search(low):
            tag = '[short pause] [warmly]'
        elif _ORDINAL.match(low) and not prev.endswith(':'):
            tag = '[short pause]'                       # list items always get a beat
        elif since < 2:
            tag = None                                  # otherwise keep tags at least two sentences apart
        elif s.endswith('?'):
            tag = '[thoughtful]'
        elif _CALM.match(low):
            tag = '[calmly]'
        elif _KEY.search(low):
            tag = '[short pause] [slowly]'
        elif prev.endswith(':') and len(prev.split()) > 3:
            tag = '[slowly]'                            # the point a lead-in like "Temel kural şudur:" announces
        elif _TURN.match(low) and since >= 3:
            tag = '[short pause]'
        out.append(f'{tag} {s}' if tag else s)
        since = 0 if tag else since + 1
    return ' '.join(out)


# ---------------------------------------------------------------- models

def _context(n, total):
    where = 'the first slide' if n == 1 else 'the last slide' if n == total else f'slide {n} of {total}'
    return f'This is {where}.'


def _claude(client, note, n, total):
    import anthropic
    try:
        r = client.beta.messages.create(
            model=CLAUDE_MODEL, max_tokens=16000, system=SYSTEM,
            output_config={'effort': 'low'},
            betas=['server-side-fallback-2026-07-01'], fallbacks='default',
            messages=[{'role': 'user', 'content': f'{_context(n, total)}\n\nNarration:\n{note}'}])
    except anthropic.AuthenticationError:
        raise PipelineError('Anthropic API anahtarı reddedildi. Anahtarı kontrol edin veya alanı boş bırakıp '
                            'kural tabanlı eklemeyi kullanın.')
    except anthropic.PermissionDeniedError as e:
        raise PipelineError(f'Anthropic anahtarının bu işlem için izni yok: {e.message}')
    if r.stop_reason == 'refusal':
        return None
    return ''.join(b.text for b in r.content if b.type == 'text')


def _openai(client, note, n, total, model):
    r = client.responses.create(model=model, instructions=SYSTEM,
                                input=f'{_context(n, total)}\n\nNarration:\n{note}')
    return r.output_text


def _openai_model(client):
    import openai
    for m in OPENAI_MODELS:
        try:
            client.models.retrieve(m)
            return m
        except openai.AuthenticationError:
            raise PipelineError('OpenAI API anahtarı reddedildi. Anahtarı kontrol edin veya alanı boş bırakıp '
                                'kural tabanlı eklemeyi kullanın.')
        except openai.NotFoundError:
            continue
    raise PipelineError(f'OpenAI hesabınızda {", ".join(OPENAI_MODELS)} modellerinden hiçbiri bulunamadı. '
                        'SLIDE2VIDEO_OPENAI_MODEL ile başka bir model adı verebilirsiniz.')


def tag_notes(slides, key='', report=None):
    """slides: visible slides with notes. Returns ({slide_no: tagged_text}, info)."""
    voiced = [s for s in slides if s['notes']]
    total = max((s['slide'] for s in slides), default=0)
    first = voiced[0]['slide'] if voiced else None
    last = voiced[-1]['slide'] if voiced else None
    key = (key or '').strip()
    method = 'kural'
    call = None
    if key:
        if provider(key) == 'anthropic':
            import anthropic
            client = anthropic.Anthropic(api_key=key, max_retries=4)
            method, call = 'Claude', lambda s: _claude(client, s['notes'], s['slide'], total)
        else:
            import openai
            client = openai.OpenAI(api_key=key, max_retries=4)
            model = _openai_model(client)
            method, call = 'OpenAI ' + model, lambda s: _openai(client, s['notes'], s['slide'], total, model)

    result, fallback, kept, done = {}, [], [], 0

    def one(s):
        if has_tags(s['notes']):
            return s['slide'], s['notes'], 'kept'
        rules = rule_tags(s['notes'], first=s['slide'] == first, last=s['slide'] == last)
        if not call:
            return s['slide'], rules, 'rules'
        try:
            text = call(s)
        except PipelineError:
            raise
        except Exception as e:
            print(f'tagging slide {s["slide"]}: {type(e).__name__}: {e}')
            text = None
        cleaned = _clean(text, s['notes']) if text else None
        return (s['slide'], cleaned, 'model') if cleaned else (s['slide'], rules, 'fallback')

    with concurrent.futures.ThreadPoolExecutor(max_workers=4 if call else 1) as ex:
        futures = [ex.submit(one, s) for s in voiced]
        try:
            for fut in concurrent.futures.as_completed(futures):
                n, text, how = fut.result()
                result[n] = text
                if how == 'fallback':
                    fallback.append(n)
                elif how == 'kept':
                    kept.append(n)
                done += 1
                if report:
                    report(done, len(voiced), n)
        except Exception:
            for f in futures:
                f.cancel()
            raise
    return result, {'method': method, 'fallback': sorted(fallback), 'kept': sorted(kept)}
