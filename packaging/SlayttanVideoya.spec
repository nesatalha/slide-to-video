# PyInstaller spec: one-folder app with Python, dependencies, static/ and ffmpeg bundled.
# Build with packaging/build.py (or: pyinstaller --noconfirm packaging/SlayttanVideoya.spec).
import os
import sys
from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files

ROOT = Path(SPECPATH).parent
mac = sys.platform == 'darwin'

datas = [(str(ROOT / 'static'), 'static')]
datas += collect_data_files('imageio_ffmpeg', subdir='binaries')  # the ffmpeg executable
datas += collect_data_files('certifi')

a = Analysis(
    [str(ROOT / 'launcher.py')],
    pathex=[str(ROOT)],
    datas=datas,
    hiddenimports=['app', 'pipeline', 'tagging'],
    # pymupdf depends on these for OCR/layout features the app never uses.
    excludes=['onnxruntime', 'networkx', 'tkinter', 'matplotlib', 'IPython', 'pytest'],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SlayttanVideoya',
    console=not mac,  # Windows: the console window is how the user sees the app is running and closes it
    upx=False,
)
coll = COLLECT(exe, a.binaries, a.datas, name='SlayttanVideoya', upx=False)

if mac:
    app = BUNDLE(
        coll,
        name='Slayttan Videoya.app',
        bundle_identifier='com.nesatalha.slayttanvideoya',
        version=os.environ.get('SLIDE2VIDEO_VERSION', '0.0.0'),
        info_plist={
            'CFBundleDisplayName': 'Slayttan Videoya',
            'NSAppleEventsUsageDescription': 'Slaytları görüntüye çevirmek için Keynote kullanılır.',
            'NSHighResolutionCapable': True,
        },
    )
