#!/bin/bash
# Slayttan Videoya uygulamasını http://127.0.0.1:8765 adresinde başlatır.
set -e
cd "$(dirname "$0")"

if [ "$(uname)" != "Darwin" ]; then
  echo "Bu uygulama şimdilik yalnızca macOS'ta çalışır (slaytlar Keynote ile dışa aktarılıyor)."; exit 1
fi
if [ ! -d "/Applications/Keynote.app" ]; then
  echo "Keynote bulunamadı. App Store'dan ücretsiz yükleyin: https://apps.apple.com/app/keynote/id409183694"; exit 1
fi
if ! python3 -c 'import sys; sys.exit(sys.version_info < (3, 10))' 2>/dev/null; then
  echo "Python 3.10 veya üstü gerekli: https://www.python.org/downloads/"; exit 1
fi

if [ ! -x .venv/bin/python ]; then
  echo "İlk kurulum yapılıyor (bir kez, birkaç dakika sürebilir)..."
  python3 -m venv .venv
fi
.venv/bin/python -c "import flask, pptx, pymupdf, imageio_ffmpeg, requests" 2>/dev/null \
  || .venv/bin/pip install --no-cache-dir -r requirements.txt

(sleep 1.5 && open http://127.0.0.1:8765) &
echo "Uygulama açılıyor: http://127.0.0.1:8765  (kapatmak için Ctrl+C)"
exec .venv/bin/python app.py
