# Implementing the provided logic to transform `test_modify.txt` into the format specified by `vspy_rx_template.txt`.
import re  # 정규표현식 모듈 추가

# 파일 경로
import sys
if len(sys.argv) > 1:
    origin_path = sys.argv[1]
else:
    print("경고: 명령줄 인자가 필요합니다. 변환할 파일 이름이나 경로를 입력하세요.")
    sys.exit(1)  # 비정상 종료

import os
working_path = os.path.splitext(origin_path)[0] + "_VspyRx" + os.path.splitext(origin_path)[1]

# Paths to the test files
input_file_path = origin_path
template_file_path = "vspy_rx_template.txt"
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

def generate_msgsig_entries(reqid, data_lines):
    entries = []
    msg_sig_counter = 0

    for line in data_lines:
        if line[0] == reqid:
            entry = {
                '#1': reqid,
                '#2': line[1] if len(line) > 1 else "",
                '#3': line[2] if len(line) > 2 else "",
                '#4': line[3] if len(line) > 3 else "",
                '#5': line[4] if len(line) > 4 else "",
                '#6': line[5] if len(line) > 5 else "",
                '#7': line[6] if len(line) > 6 else "",
                '#8': line[7] if len(line) > 7 else "",
                '#9': line[8] if len(line) > 8 else "",
                '@1': msg_sig_counter,
            }
            msg_sig_counter += 1
            entries.append(entry)
    return entries

def remove_empty_lines(formatted_msgs):
    """
    Remove lines with empty data (e.g., <ByteString4></ByteString5>) from each message.
    """
    cleaned_msgs = []
    for msg in formatted_msgs:
        # Remove lines matching empty placeholders
        cleaned_msg = "\n".join([line for line in msg.splitlines() if not re.search(r"<.*?>\s*</.*?>", line.strip())])
        cleaned_msgs.append(cleaned_msg)
    return cleaned_msgs


def format_vspy_rx_template(system, rspid, entries, template_path, output_path):
    with open(template_path, 'r') as file:
        template = file.read()

    formatted_msgs = []

    for entry in entries:
        formatted_msg = template
        formatted_msg = formatted_msg.replace("!1", system)
        formatted_msg = formatted_msg.replace("$1", rspid)
        for key, value in entry.items():
            formatted_msg = formatted_msg.replace(key, str(value))
        formatted_msgs.append(formatted_msg)
    
    # Remove empty lines from each formatted message
    cleaned_msgs = remove_empty_lines(formatted_msgs)

    with open(output_path, 'w') as file:
        file.write("\n".join(cleaned_msgs))

    return cleaned_msgs


# Parse input file
reqid, rspid, system, data_lines = parse_input_file(input_file_path)
print(f"Extracted REQID: {reqid}, RSPID: {rspid}, SYSTEM_NAME: {system}")  # 디버깅 출력

# Generate message signature entries
msgsig_entries = generate_msgsig_entries(reqid, data_lines)

# Format and write the output
formatted_output = format_vspy_rx_template(system, rspid, msgsig_entries, template_file_path, output_file_path)

# Returning the formatted output to user
#formatted_output
