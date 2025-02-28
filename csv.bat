@echo off
chcp 65001 >nul  & REM UTF-8 인코딩 설정
SETLOCAL ENABLEDELAYEDEXPANSION

:: 파일 이름을 입력했는지 확인
IF "%~1"=="" (
    echo 사용법: csv2txt.bat 파일명.csv
    exit /b 1
)

:: 입력된 파일명 가져오기
SET FILENAME1=%~1
SET FILENAME2=%~n11%~x1
SET FILENAME3=%~n112%~x1

:: 라인 제거 스크립트 실행
python csv1.py "%FILENAME1%.csv"

:: 컬럼 제거 실행
python csv2.py "%FILENAME2%.csv"

:: 첫 라인 필터 설정 후 .xlsx 형식으로 저장
python csv3.py "%FILENAME3%.csv"


:: 임시 파일 삭제 (나중에 디버깅시에는 주석 처리 해서 단계별로 확인 필요)
IF EXIST "%FILENAME2%.csv" del "%FILENAME2%.csv"
IF EXIST "%FILENAME3%.csv" del "%FILENAME3%.csv"

:: FILENAME3.xlsx → FILENAME1.xlsx 으로 리네임
IF EXIST "%FILENAME3%.xlsx" (
    ren "%FILENAME3%.xlsx" "%FILENAME1%.xlsx"
    echo ✅ %FILENAME3%.xlsx has been renamed to %FILENAME1%.xlsx
) ELSE (
    echo ❌ %FILENAME3%.xlsx does not exist!
)

echo ✅ 배치 파일 1,2,3 작업이 완료되었습니다.

ENDLOCAL
