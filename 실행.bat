@echo off
chcp 65001 > nul
echo ============================================================
echo Word 문서 이미지 추출 및 분석 도구
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
pip show pillow > nul 2>&1
if errorlevel 1 (
    echo pillow 라이브러리 설치 중...
    pip install pillow
)

pip show openpyxl > nul 2>&1
if errorlevel 1 (
    echo openpyxl 라이브러리 설치 중...
    pip install openpyxl
)

pip show python-docx > nul 2>&1
if errorlevel 1 (
    echo python-docx 라이브러리 설치 중...
    pip install python-docx
)

echo.
echo 라이브러리 설치 완료!
echo.
echo ============================================================
echo 프로그램 실행 중...
echo ============================================================
echo.

REM Python 스크립트 실행
python extract_images_from_word.py

echo.
pause
