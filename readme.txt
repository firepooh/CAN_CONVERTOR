@ 파일 변환 과정
1. vspy 프로그램내에서 (*.vsb)로그 파일을 (*.csv) 형태로 변환
   ex> bcm.vsb -> bcm.csv

2. conv_csv2txt.py : csv 필요없는 행 제거
   ex> conv_csv2txt.py bcm.vsb       : default 설정된 라인 제거(1~134)
       conv_csv2txt.py bcm.vsb 1-100 : 1~100 라인제거
       bcm1.csv : 출력물
  
3. conv_csv2txt2.py : csv 필요없는 컬럼 제거
   ex> conv_csv2txt2.py bcm1.vsb       : default 설정된 컬럼 제거("Line", "Abs Time(Sec)", "Rel Time (Sec)", "Status", "Er","Tx","Description","Network","Node","Trgt","Src","Value","Trigger","Signals")
       conv_csv2txt.py bcm1.vsb Line,Status : Line,Status 컬럼 제거
       bcm12.csv : 출력물

4. csv2txt.bat : 2번, 3번을 한번에 실행 해주는 배치 파일
   ex> csv2txt.bat bcm.csv
       bcm1.csv : 출력물
       bcm12.csv : 출력물
