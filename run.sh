#!/bin/bash
# Slayttan Videoya uygulamasını http://127.0.0.1:8765 adresinde başlatır.
set -e
cd "$(dirname "$0")"

has_keynote=0
if [ "$(uname)" = "Darwin" ] && { [ -d "/Applications/Keynote.app" ] || [ -d "$HOME/Applications/Keynote.app" ]; }; then
  has_keynote=1
fi
if [ $has_keynote = 0 ] && ! command -v soffice >/dev/null && ! command -v libreoffice >/dev/null \
   && [ ! -x "/Applications/LibreOffice.app/Contents/MacOS/soffice" ] && ! ls /opt/libreoffice*/program/soffice >/dev/null 2>&1; then
  echo "Slaytları dışa aktarmak için Keynote (yalnızca macOS) veya LibreOffice gerekli."
  echo "  macOS: Keynote'u App Store'dan ücretsiz yükleyin: https://apps.apple.com/app/keynote/id409183694"
  echo "  Diğer: LibreOffice'i yükleyin: https://www.libreoffice.org/download/"
  exit 1
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

(sleep 1.5 && { command -v open >/dev/null && open http://127.0.0.1:8765 || xdg-open http://127.0.0.1:8765; } >/dev/null 2>&1) &
echo "Uygulama açılıyor: http://127.0.0.1:8765  (kapatmak için Ctrl+C)"
exec .venv/bin/python app.py
