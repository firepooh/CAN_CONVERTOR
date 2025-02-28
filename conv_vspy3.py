import argparse
import os

def insert_data(template_file, msgsigs_file, txmsgs_file, output_file):
    """vspy_template.txt에 MsgSigs 및 TxMsgs 내용을 삽입하여 새로운 파일로 저장"""
    
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
    parser = argparse.ArgumentParser(description="vspy_template.txt 파일에 입력파일1과 입력파일2 내용을 삽입하여 새로운 파일 생성")
    parser.add_argument("template_file", help="vspy_template.txt 파일 경로")
    parser.add_argument("msgsigs_file", help="입력 파일1 (MsgSigs에 삽입할 파일) 경로")
    parser.add_argument("txmsgs_file", help="입력 파일2 (TxMsgs에 삽입할 파일) 경로")
    parser.add_argument("output_file", help="출력 파일 경로")

    args = parser.parse_args()
    
    insert_data(args.template_file, args.msgsigs_file, args.txmsgs_file, args.output_file)
