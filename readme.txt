@ 파이썬 추가 설치 필요한 라이브러리
========================================================================================
pip install pandas
pip install openpyxl
========================================================================================



@ 1차 파일 변환 과정. (vspy log 파일에서 필요한 canid 데이터만 추출하여 txt로 저장)
========================================================================================
1. vspy 프로그램에서 (*.vsb) 로그 파일을 (*.csv) 형태로 변환(수동변환)
ex> bcm.vsb -> bcm.csv

2. csv1.py : csv 필요없는 라인(헤더) 제거
ex> csv1.py bcm.csv       : default 설정된 라인 제거(1~134)
    csv1.py bcm.vsb 1-100 : 1~100 선택 라인 제거
    bcm1.csv : 출력물
  
3. csv2.py : csv 필요없는 컬럼 제거
ex> csv2.py bcm1.csv       : default 설정된 컬럼 제거 ("Line", "Abs Time(Sec)", "Rel Time (Sec)", "Status", "Er","Tx","Description","Network","Node","Trgt","Src","Value","Trigger","Signals")
    csv2.py bcm1.csv Line,Status : Line,Status 선택 컬럼 제거
    bcm12.csv : 출력물

4. csv3.py : 행,컬럼 제거된 csv에서 첫 라인을 필터로 설정 후 .xlsx 로 저장

5. csv.bat : 2,3,4번 작업을 한번에 실행 해주는 배치 파일
   최종 출력물 .xlsx파일에서 필요한 can id만 필터 설정 후 copy 하여 txt로 저장한다.
   *.csv 파일 입력시 확장자 지정 하지않고 이름만 입력 한다.
ex> csv.bat bcm
    bcm.xlsx : 출력물
    bcm.txt : 출력물 엑셀에서 수동 필터 적용후 선택 지정하여 copy 하여 txt로 저장.(수동)
========================================================================================
   


@ 2차 파일 변환 과정.(1차 파일 변환 과정에서 생성된 txt파일로부터 vspy simulator에 필요한 tx/rx xml 추출 )
========================================================================================
1. 1차에서 변환된 txt파일에 추가 정보 입력
ex> 
PT	   B1	B2	B3	B4	B5	B6	B7	B8
754	1	3E	00	00	00	00	00	00
75C	1	7E	00	00	00	00	00	00
754	2	A8	01	00	00	00	00	00

-> 수동으로 추가 정보 입력(reqid,rspid,system name). 추가 정보 입력시 'space'사용 하면 안되고
   반드시 'tab'으로 분리 해야함.

reqid	754
rspid	75C
system	BCM
PT	B1	B2	B3	B4	B5	B6	B7	B8
754	1	3E	00	00	00	00	00	00
75C	1	7E	00	00	00	00	00	00
754	2	A8	01	00	00	00	00	00

2. conv_vspy.py : can log data 에서 vspy에 맞게 
