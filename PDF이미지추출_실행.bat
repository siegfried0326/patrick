@echo off
chcp 65001 > nul
echo ============================================================
echo PDF 이미지 추출 도구
echo ============================================================
echo.

REM Python 설치 확인
python --version > nul 2>&1
if errorlevel 1 (
    echo [오류] Python이 설치되어 있지 않습니다.
    echo Python을 먼저 설치해주세요: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Python 확인 완료!
echo.

REM 필요한 라이브러리 설치 확인 및 설치
echo 필요한 라이브러리 확인 중...

pip show PyMuPDF > nul 2>&1
if errorlevel 1 (
    echo PyMuPDF 라이브러리 설치 중...
    pip install PyMuPDF
)

pip show Pillow > nul 2>&1
if errorlevel 1 (
    echo Pillow 라이브러리 설치 중...
    pip install Pillow
)

echo.
echo 라이브러리 설치 완료!
echo.
echo ============================================================
echo 프로그램 실행 중...
echo ============================================================
echo.

REM Python 스크립트 실행
python extract_images_from_pdf.py

echo.
pause
