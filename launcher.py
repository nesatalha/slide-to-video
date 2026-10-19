"""Entry point of the packaged app (SlayttanVideoya.exe / Slayttan Videoya.app).

Stores data in a user-writable folder, serves the app on http://127.0.0.1:8765,
opens the browser and tells the user how to close it:
  Windows: a console window ("close this window to quit")
  macOS:   a small dialog with "Tarayıcıda aç" / "Kapat" buttons
Running `python launcher.py` from source works too (data then goes to the same user folder).
"""
import os
import subprocess
import sys
import threading
import time
import urllib.request
import webbrowser
from pathlib import Path

NAME = 'Slayttan Videoya'
HOST, PORT = '127.0.0.1', 8765
URL = f'http://{HOST}:{PORT}'
MAC_APP = sys.platform == 'darwin' and getattr(sys, 'frozen', False)


def data_dir():
    if os.environ.get('SLIDE2VIDEO_DATA'):
        return Path(os.environ['SLIDE2VIDEO_DATA'])
    if sys.platform == 'win32':
        base = Path(os.environ.get('LOCALAPPDATA') or Path.home() / 'AppData/Local')
    elif sys.platform == 'darwin':
        base = Path.home() / 'Library/Application Support'
    else:
        base = Path(os.environ.get('XDG_DATA_HOME') or Path.home() / '.local/share')
    return base / 'SlayttanVideoya'


def already_running():
    try:
        with urllib.request.urlopen(URL + '/api/config', timeout=2) as r:
            return r.status == 200
    except Exception:
        return False


def mac_dialog(text, buttons):
    """Show a native dialog and return the clicked button ('' if it could not be shown)."""
    btns = ', '.join(f'"{b}"' for b in buttons)
    script = (f'display dialog "{text}" with title "{NAME}" buttons {{{btns}}} '
              f'default button "{buttons[0]}" with icon note')
    r = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    return r.stdout.strip().removeprefix('button returned:') if r.returncode == 0 else ''


def tell(text):
    """Message the user and wait until they've read it (dialog on macOS, console elsewhere)."""
    if MAC_APP:
        mac_dialog(text, ['Tamam'])
    else:
        print(text)
        try:
            input('\nPencereyi kapatmak için Enter tuşuna basın.')
        except EOFError:
            pass


def main():
    data = data_dir()
    data.mkdir(parents=True, exist_ok=True)
    os.environ['SLIDE2VIDEO_DATA'] = str(data)
    if sys.stdout is None or sys.stderr is None:  # windowed build: keep a log for troubleshooting
        log = open(data / 'log.txt', 'a', encoding='utf-8', buffering=1)
        sys.stdout = sys.stdout or log
        sys.stderr = sys.stderr or log
    for stream in (sys.stdout, sys.stderr):  # Turkish text must not crash when output goes to a pipe or file
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8', errors='replace')
    if sys.platform == 'win32':
        try:
            import ctypes
            ctypes.windll.kernel32.SetConsoleTitleW(NAME)
        except Exception:
            pass

    if already_running():
        webbrowser.open(URL)
        if not MAC_APP:
            print(f'{NAME} zaten açık; tarayıcıda gösteriliyor: {URL}')
            time.sleep(3)
        return

    from werkzeug.serving import make_server
    import app
    try:
        server = make_server(HOST, PORT, app.app, threaded=True)
    except OSError:
        tell(f'{NAME} açılamadı: {PORT} numaralı bağlantı noktası başka bir program tarafından kullanılıyor.\n\n'
             'Bilgisayarı yeniden başlatıp tekrar deneyin.')
        sys.exit(1)
    app.load_jobs()
    threading.Timer(1, webbrowser.open, [URL]).start()

    if MAC_APP:
        threading.Thread(target=server.serve_forever, daemon=True).start()
        text = (f'{NAME} çalışıyor ve tarayıcınızda açıldı:\\n{URL}\\n\\n'
                'İşiniz bitince Kapat düğmesine basın. Video hazırlanırken kapatmayın.')
        while True:
            choice = mac_dialog(text, ['Tarayıcıda aç', 'Kapat'])
            if choice == 'Kapat':
                break
            if choice == 'Tarayıcıda aç':
                webbrowser.open(URL)
            else:
                time.sleep(1)
        server.shutdown()
        return

    print('=' * 60)
    print(f'  {NAME} çalışıyor: {URL}')
    print('  Uygulama tarayıcınızda açılacak.')
    print('  İşiniz bitince bu pencereyi kapatın (sağ üstteki X).')
    print('  Video hazırlanırken bu pencereyi kapatmayın.')
    print('=' * 60)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
