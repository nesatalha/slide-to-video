"""Build the packaged app and zip it for a GitHub Release.

    python packaging/build.py [version]

Needs the app's requirements plus PyInstaller (packaging/requirements-build.txt).
Output: dist/SlayttanVideoya-<windows|macos>-<arch>.zip
  Windows: SlayttanVideoya/SlayttanVideoya.exe (+ _internal/)
  macOS:   Slayttan Videoya.app
"""
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / 'dist'


def main():
    version = (sys.argv[1] if len(sys.argv) > 1 else os.environ.get('SLIDE2VIDEO_VERSION', '0.0.0')).lstrip('v')
    env = dict(os.environ, SLIDE2VIDEO_VERSION=version)
    subprocess.run([sys.executable, '-m', 'PyInstaller', '--noconfirm', '--clean',
                    '--distpath', str(DIST), '--workpath', str(ROOT / 'build'),
                    str(ROOT / 'packaging/SlayttanVideoya.spec')], check=True, cwd=ROOT, env=env)

    arch = {'amd64': 'x64', 'x86_64': 'x64', 'arm64': 'arm64', 'aarch64': 'arm64'}.get(platform.machine().lower(),
                                                                                         platform.machine())
    if sys.platform == 'darwin':
        zip_path = DIST / f'SlayttanVideoya-macos-{arch}.zip'
        zip_path.unlink(missing_ok=True)
        # ditto keeps the bundle's symlinks and code signature intact (zipfile would not).
        subprocess.run(['ditto', '-c', '-k', '--sequesterRsrc', '--keepParent',
                        str(DIST / 'Slayttan Videoya.app'), str(zip_path)], check=True)
    else:
        name = 'windows' if sys.platform == 'win32' else sys.platform
        zip_path = Path(shutil.make_archive(str(DIST / f'SlayttanVideoya-{name}-{arch}'), 'zip',
                                            DIST, 'SlayttanVideoya'))
    print(f'Hazır: {zip_path} ({zip_path.stat().st_size // 2**20} MB)')


if __name__ == '__main__':
    main()
