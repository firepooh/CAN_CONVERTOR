@echo off
chcp 65001 >nul  & REM UTF-8 인코딩 설정
SETLOCAL ENABLEDELAYEDEXPANSION

:: 파일 이름을 입력했는지 확인
IF "%~1"=="" (
    echo 사용법: vspy.bat 파일명.txt
    exit /b 1
)

:: 입력된 파일명 가져오기
SET FILENAME1=%~1

:: vspy rx
python vspy2rx.py "%FILENAME1%.txt"

:: vspy tx
python vspy3tx.py "%FILENAME1%.txt"

:: 최종 vspy 파일 생성
python vspy4.py %FILENAME1%

:: 임시 파일 삭제 (나중에 디버깅시에는 주석 처리 해서 단계별로 확인 필요)
IF EXIST "%FILENAME1%_VspyRx.txt" del "%FILENAME1%_VspyRx.txt"
IF EXIST "%FILENAME1%_VspyTx.txt" del "%FILENAME1%_VspyTx.txt"

echo ✅ 배치 파일 1,2,3 작업이 완료되었습니다.

ENDLOCAL
