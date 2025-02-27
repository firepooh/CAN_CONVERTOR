import pandas as pd
import os
import argparse

# 기본적으로 삭제할 컬럼 목록 (사용자가 입력하지 않아도 삭제됨)
DEFAULT_COLUMNS = ["Line", "Abs Time(Sec)", "Rel Time (Sec)", "Status", "Er","Tx","Description","Network","Node",
                   "Trgt","Src","Value","Trigger","Signals" ]  # 필요에 따라 컬럼 추가 가능

def delete_columns(file_path, columns_to_delete):
    """CSV 파일에서 기본 컬럼 + 사용자 지정 컬럼을 삭제하고 '2.csv'로 저장"""
    try:
        # CSV 파일 읽기
        df = pd.read_csv(file_path, delimiter=",")

        # 현재 컬럼 목록 출력
        available_columns = list(df.columns)
        print("\n📌 현재 컬럼 목록:", available_columns, "\n")

        # 사용자 입력 컬럼 처리
        if columns_to_delete:
            user_columns = [col.strip() for col in columns_to_delete.split(",")]
        else:
            user_columns = []

        # 삭제할 컬럼 = 기본 컬럼 + 사용자 입력 컬럼
        columns_list = list(set(DEFAULT_COLUMNS + user_columns))

        # 선택한 컬럼 삭제 (존재하지 않는 컬럼 무시)
        df = df.drop(columns=columns_list, errors="ignore")
        print(f"✅ 삭제된 컬럼: {columns_list}\n")

        # 출력 파일명 설정 (2.csv)
        base_name, _ = os.path.splitext(file_path)
        modified_file_path = f"{base_name}2.csv"

        # 수정된 내용 저장
        df.to_csv(modified_file_path, index=False, sep=",")
        print(f"✅ 컬럼 삭제 완료! '{modified_file_path}'에 저장되었습니다.")

    except FileNotFoundError:
        print(f"❌ 오류: '{file_path}' 파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    # 명령줄 인자 파싱
    parser = argparse.ArgumentParser(description="CSV 파일에서 특정 컬럼을 삭제하고 '2.csv'로 저장합니다.")
    parser.add_argument("file", help="CSV 파일 경로 (예: data.csv)")
    parser.add_argument("columns", nargs="?", default="", help="삭제할 컬럼 이름 (쉼표로 구분, 예: A,B,C). 입력 없으면 기본 컬럼만 삭제")

    args = parser.parse_args()
    delete_columns(args.file, args.columns)
