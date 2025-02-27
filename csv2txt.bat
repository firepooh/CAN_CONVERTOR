@echo off
SETLOCAL

:: 파일 이름을 입력했는지 확인
IF "%~1"=="" (
    echo 사용법: csv2txt.bat 파일명.csv
    exit /b 1
)

:: 입력된 파일명 가져오기
SET FILENAME=%~1
SET FILENAME2=%~n11%~x1

:: 첫 번째 파이썬 스크립트 실행
python conv_csv2txt.py %FILENAME%

:: 두 번째 파이썬 스크립트 실행
python conv_csv2txt2.py %FILENAME2%

echo 모든 작업이 완료되었습니다.

ENDLOCAL
