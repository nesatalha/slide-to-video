@echo off
rem Slayttan Videoya uygulamasini http://127.0.0.1:8765 adresinde baslatir.
chcp 65001 >nul
setlocal
cd /d "%~dp0"

set "SOFFICE="
where soffice >nul 2>&1
if not errorlevel 1 set "SOFFICE=soffice"
if not defined SOFFICE if exist "%ProgramFiles%\LibreOffice\program\soffice.exe" set "SOFFICE=%ProgramFiles%\LibreOffice\program\soffice.exe"
if not defined SOFFICE if exist "%ProgramFiles(x86)%\LibreOffice\program\soffice.exe" set "SOFFICE=%ProgramFiles(x86)%\LibreOffice\program\soffice.exe"
if not defined SOFFICE (
  echo Slaytları dışa aktarmak için LibreOffice gerekli: https://www.libreoffice.org/download/
  pause
  exit /b 1
)

set "PY="
where py >nul 2>&1
if not errorlevel 1 set "PY=py -3"
if not defined PY (
  where python >nul 2>&1
  if not errorlevel 1 set "PY=python"
)
if not defined PY (
  echo Python 3.10 veya üstü gerekli: https://www.python.org/downloads/
  pause
  exit /b 1
)
%PY% -c "import sys; sys.exit(sys.version_info < (3, 10))" >nul 2>&1
if errorlevel 1 (
  echo Python 3.10 veya üstü gerekli: https://www.python.org/downloads/
  pause
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo İlk kurulum yapılıyor ^(bir kez, birkaç dakika sürebilir^)...
  %PY% -m venv .venv || (pause & exit /b 1)
)
".venv\Scripts\python.exe" -c "import flask, pptx, pymupdf, imageio_ffmpeg, requests, anthropic, openai" >nul 2>&1
if errorlevel 1 (
  ".venv\Scripts\python.exe" -m pip install --no-cache-dir -r requirements.txt || (pause & exit /b 1)
)

start "" /b powershell -NoProfile -Command "Start-Sleep -Seconds 2; Start-Process 'http://127.0.0.1:8765'"
echo Uygulama açılıyor: http://127.0.0.1:8765  (kapatmak için Ctrl+C)
".venv\Scripts\python.exe" app.py
pause
