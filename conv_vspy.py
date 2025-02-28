import pandas as pd

# 파일 경로
import sys
if len(sys.argv) > 1:
    origin_path = sys.argv[1]
else:
    print("경고: 명령줄 인자가 필요합니다. 변환할 파일 이름이나 경로를 입력하세요.")
    sys.exit(1)  # 비정상 종료
import os
working_path = os.path.splitext(origin_path)[0] + "1" + os.path.splitext(origin_path)[1]

# 파일 읽기
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

# reqid, rspid, system 추출 함수
def extract_ids(data):
    reqid = None
    rspid = None
    system = None
    for line in data[:3]:
        if 'reqid' in line:
            reqid = line.strip().split('\t')[1]
        if 'rspid' in line:
            rspid = line.strip().split('\t')[1]
        if 'system' in line:
            system = line.strip().split('\t')[1]

    # 유효성 검사
    if reqid is None or rspid is None or system is None:
        print("경고: reqid, rspid, 또는 system 값이 누락되었습니다. 프로그램을 종료합니다.")
        print("VSPY에서 변환된 파일에서, 3가지 항목을 수동 기입해야 합니다.")
        print("ex) 탭으로 분리 합니다. Space로 분리하면 안됩니다. ")
        print("reqid\t0x10")
        print("rspid\t0x20")
        print("system\tBMS")
        sys.exit(1)  # 비정상 종료

    return reqid, rspid, system

# 중복 제거 후 빈 라인으로 대체
def remove_duplicates_with_blanks(data):
    unique_lines = []
    seen_lines = set()
    for line in data:
        if line not in seen_lines:
            unique_lines.append(line)
            seen_lines.add(line)
        else:
            unique_lines.append('\n')
    return unique_lines

# reqid로 시작하는 라인에서 B1이 0x30일 때 삭제하는 함수
def remove_lines_with_b1_30(data, reqid):
    filtered_lines = []
    for line in data:
        if line.startswith(reqid):
            parts = line.strip().split('\t')
            if len(parts) > 1 and int(parts[1], 16) == 0x30:
                continue
        if line.strip():  # 빈 줄이 아닌 경우에만 추가
            filtered_lines.append(line)
    return filtered_lines

# rspid로 시작하는 라인에서 B2 == 0x7F && B4 == 0x78 일 때 삭제하는 함수
def remove_lines_with_flowcontrol(data, rspid):
    filtered_lines = []
    for line in data:
        if line.startswith(rspid):
            parts = line.strip().split('\t')
            if len(parts) > 4 and int(parts[2], 16) == 0x7F and int(parts[4], 16) == 0x78:
                continue
        if line.strip():  # 빈 줄이 아닌 경우에만 추가
            filtered_lines.append(line)
    return filtered_lines

# 특정 ID로 시작하는 라인의 유효한 데이터 외 00으로 채워진 부분 삭제하는 함수 (B1 < 10일 때만 적용)
def trim_trailing_zeros(data, identifier):
    trimmed_lines = []
    for line in data:
        if line.startswith(identifier):
            parts = line.strip().split('\t')
            data_length = int(parts[1], 16)  # B1 데이터 길이
            if data_length < 0x10:  # B1이 10(hex)보다 작은 경우만 적용
                actual_data = parts[:2 + data_length]  # 데이터 길이만큼 잘라서 유지
                trimmed_line = '\t'.join(actual_data) + '\n'
                trimmed_lines.append(trimmed_line)
            else:
                trimmed_lines.append(line)
        else:
            trimmed_lines.append(line)
    return trimmed_lines

# rspid로 시작하는 라인에서 B1이 20~2F 사이일 경우 윗 라인에 데이터 병합
def merge_rspid_lines(data, rspid):
    merged_lines = []
    i = 0
    while i < len(data):
        line = data[i]
        if line.startswith(rspid):
            parts = line.strip().split('\t')
            b1_value = int(parts[1], 16)
            if 0x20 <= b1_value <= 0x2F:
                # rspid와 B1 삭제 후 나머지 데이터 윗 라인에 병합
                if merged_lines:
                    merged_lines[-1] = merged_lines[-1].strip() + '\t' + '\t'.join(parts[2:]) + '\n'
                i += 1
                continue
        merged_lines.append(line)
        i += 1
    return merged_lines

# rspid로 시작하는 라인 중 B1이 10일 경우 B1만 삭제하는 함수
def remove_b1_10(data, rspid):
    modified_lines = []
    for line in data:
        if line.startswith(rspid):
            parts = line.strip().split('\t')
            if parts[1] == '10':
                modified_line = parts[0] + '\t' + '\t'.join(parts[2:]) + '\n'
                modified_lines.append(modified_line)
            else:
                modified_lines.append(line)
        else:
            modified_lines.append(line)
    return modified_lines

# rspid로 시작하는 라인의 유효한 데이터 외 00으로 채워진 부분 삭제하는 함수 (B1 조건 없이 적용)
def trim_trailing_zeros_rspid(data, rspid):
    trimmed_lines = []
    for line in data:
        if line.startswith(rspid):
            parts = line.strip().split('\t')
            data_length = int(parts[1], 16)  # B1 데이터 길이
            actual_data = parts[:2 + data_length]  # 데이터 길이만큼 잘라서 유지
            trimmed_line = '\t'.join(actual_data) + '\n'
            trimmed_lines.append(trimmed_line)
        else:
            trimmed_lines.append(line)
    return trimmed_lines

# reqid와 rspid를 1pair로 구분하는 함수
def add_blank_after_rspid(data, reqid, rspid):
    processed_lines = []
    for i in range(len(data)):
        processed_lines.append(data[i])
        if data[i].startswith(rspid) and i > 0 and data[i - 1].startswith(reqid):
            processed_lines.append('\n')  # rspid 뒤에 빈 줄 추가
    return processed_lines

# reqid로 시작하는 라인을 중복 검사하고 중복 및 다음 라인 삭제
def remove_duplicate_reqid_and_next(data, reqid):
    filtered_lines = []
    skip_next = False
    seen_lines = set()

    for i in range(len(data)):
        line = data[i]
        if skip_next:
            skip_next = False
            continue

        if line.startswith(reqid):
            if line in seen_lines:
                skip_next = True  # 다음 라인도 삭제
                continue
            seen_lines.add(line)
        filtered_lines.append(line)

    return filtered_lines

# 결과 파일 저장
def save_file(data, output_path):
    with open(output_path, 'w') as file:
        file.writelines(data)

# 실행 부분
origin_data = read_file(origin_path)

reqid, rspid, system = extract_ids(origin_data)
print(f"reqid: {reqid}, rspid: {rspid}, system: {system}")

#modify_data = remove_duplicates_with_blanks(origin_data)

modify_data = remove_lines_with_flowcontrol(origin_data, rspid)

modify_data = remove_lines_with_b1_30(modify_data, reqid)

modify_data = trim_trailing_zeros(modify_data, reqid)

modify_data = trim_trailing_zeros(modify_data, rspid)

modify_data = merge_rspid_lines(modify_data, rspid)

modify_data = remove_b1_10(modify_data, rspid)

modify_data = trim_trailing_zeros_rspid(modify_data, rspid)

modify_data = add_blank_after_rspid(modify_data, reqid, rspid)

modify_data = remove_duplicate_reqid_and_next(modify_data, reqid)

output_path = working_path

save_file(modify_data, output_path)

output_path
