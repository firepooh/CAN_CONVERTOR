@ 파일 변환 과정
1. vspy 프로그램내에서 (*.vsb)로그 파일을 (*.csv) 형태로 변환
   ex> bcm.vsb -> bcm.csv

2. conv_csv2txt.py 변환 프로그램으로 csv 필요없는 행 제거
   ex> conv_csv2txt.py bcm.vsb       : 1~134 라인제거(default)
       conv_csv2txt.py bcm.vsb 1-100 : 1~100 라인제거

3. conv_csv2txt2.py 변환 프로그램으로 csv 필요없는 컬럼 제거


