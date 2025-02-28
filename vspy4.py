import argparse
import os

def insert_data(base_filename):
    """'vspy_template.txt'에 MsgSigs 및 TxMsgs 내용을 삽입하여 새로운 파일로 저장"""

    template_file = "vspy_template.txt"  # 템플릿 파일 고정
    msgsigs_file = f"{base_filename}_VspyRx.txt"  # 첫 번째 입력 파일
    txmsgs_file = f"{base_filename}_VspyTx.txt"  # 두 번째 입력 파일
    output_file = f"{base_filename[:-1]}.vs3"  # 출력 파일 (마지막 숫자 제거)

    # 템플릿 파일 읽기
    with open(template_file, "r", encoding="utf-8") as f:
        template_content = f.read()

    # 입력파일1 (MsgSigs) 읽기
    with open(msgsigs_file, "r", encoding="utf-8") as f:
        msgsigs_content = f.read().strip()

    # 입력파일2 (TxMsgs) 읽기
    with open(txmsgs_file, "r", encoding="utf-8") as f:
        txmsgs_content = f.read().strip()

    # <MsgSigs> 태그 안에 데이터 삽입
    template_content = template_content.replace("<MsgSigs>\n</MsgSigs>", f"<MsgSigs>\n{msgsigs_content}\n</MsgSigs>")

    # <TxMsgs> 태그 안에 데이터 삽입
    template_content = template_content.replace("<TxMsgs>\n</TxMsgs>", f"<TxMsgs>\n{txmsgs_content}\n</TxMsgs>")

    # 새 파일로 저장
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(template_content)

    print(f"✅ 파일 변환 완료! 저장된 파일: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="vspy_template.txt 파일에 데이터를 삽입하여 새로운 .vs3 파일 생성")
    parser.add_argument("base_filename", help="기본 파일 이름 (예: bcm1)")

    args = parser.parse_args()
    
    insert_data(args.base_filename)
