@echo off
chcp 65001 > nul
echo ============================================================
echo Python 라이브러리 설치 도구
echo ============================================================
echo.

REM Python 설치 확인
python --version > nul 2>&1
if errorlevel 1 (
    echo [오류] Python이 설치되어 있지 않습니다.
    echo.
    echo Python 다운로드: https://www.python.org/downloads/
    echo.
    echo 설치 시 주의사항:
    echo - "Add Python to PATH" 옵션을 반드시 체크하세요!
    echo.
    pause
    exit /b 1
)

echo Python 버전:
python --version
echo.

echo ============================================================
echo 필요한 라이브러리를 설치합니다...
echo ============================================================
echo.

echo [1/3] Pillow (이미지 처리) 설치 중...
pip install pillow --upgrade
echo.

echo [2/3] openpyxl (엑셀 파일 생성) 설치 중...
pip install openpyxl --upgrade
echo.

echo [3/3] python-docx (Word 문서 처리) 설치 중...
pip install python-docx --upgrade
echo.

echo ============================================================
echo 설치 완료!
echo ============================================================
echo.

echo 설치된 라이브러리 확인:
pip list | findstr "pillow openpyxl python-docx"
echo.

echo 이제 '실행.bat' 파일을 실행하세요!
echo.
pause
