# Implementing the provided logic to transform `test_modify.txt` into the format specified by `vspy_tx_template.txt`.
import re  # 정규표현식 모듈 추가

# 파일 경로
import sys
if len(sys.argv) > 1:
    origin_path = sys.argv[1]
else:
    print("경고: 명령줄 인자가 필요합니다. 변환할 파일 이름이나 경로를 입력하세요.")
    sys.exit(1)  # 비정상 종료

import os
working_path = os.path.splitext(origin_path)[0] + "_VspyTx" + os.path.splitext(origin_path)[1]

# Paths to the test files
input_file_path = origin_path
template_file_path = "vspy_tx_template.txt"
output_file_path = working_path

def parse_input_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    reqid, rspid, system = None, None, None
    data_lines = []

    for line in lines:
        if line.startswith("reqid"):
            reqid = line.split("\t")[1].strip()
        elif line.startswith("rspid"):
            rspid = line.split("\t")[1].strip()
        elif line.startswith("system"):
            system = line.split("\t")[1].strip()
        else:
            if line.strip():  # Exclude empty lines
                data_lines.append(line.strip().split())
    
    return reqid, rspid, system, data_lines

def generate_msgsig_entries(rspid, data_lines):
    entries = []
    msg_counter = 0

    for line in data_lines:
        if line[0] == rspid:
            # Collect all data from the second item to the end
            data_string = ",".join(line[2:])
            entry = {
                "@1": msg_counter,
                "#": data_string,
                "$1": rspid,
                "%1": "True" if len(rspid) > 3 else "False",
            }
            msg_counter += 1
            entries.append(entry)
    return entries

def format_vspy_tx_template(system, rspid, entries, template_path, output_path):
    with open(template_path, 'r') as file:
        template = file.read()

    formatted_msgs = []

    for entry in entries:
        formatted_msg = template
        formatted_msg = formatted_msg.replace("!1", system)
        formatted_msg = formatted_msg.replace("$1", rspid)
        formatted_msg = formatted_msg.replace("@1", str(entry["@1"]))
        formatted_msg = formatted_msg.replace("#", entry["#"])
        formatted_msg = formatted_msg.replace("%1", entry["%1"])  # 적용된 부분
        formatted_msgs.append(formatted_msg)

    with open(output_path, 'w') as file:
        file.write("\n".join(formatted_msgs))

    return formatted_msgs

# Parse input file
reqid, rspid, system, data_lines = parse_input_file(input_file_path)
print(f"Extracted REQID: {reqid}, RSPID: {rspid}, SYSTEM_NAME: {system}")  # 디버깅 출력

# Generate message signature entries
msgsig_entries = generate_msgsig_entries(rspid, data_lines)

# Format and write the output
formatted_output = format_vspy_tx_template(system, rspid, msgsig_entries, template_file_path, output_file_path)

# Returning the formatted output to user
#formatted_output
