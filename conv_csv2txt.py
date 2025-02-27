import os
import argparse

def delete_lines(file_path, lines_to_delete):
    """TXT 파일에서 특정 라인(단일 or 범위)을 삭제하고 '_lineremove.csv'로 저장하는 함수"""
    try:
        # 파일 읽기
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # 삭제할 라인 처리
        lines_to_delete_set = set()
        for part in lines_to_delete.split(","):
            if "-" in part:  # 범위 처리 (예: 3-5)
                start, end = map(int, part.split("-"))
                lines_to_delete_set.update(range(start, end + 1))
            else:  # 단일 라인 처리
                lines_to_delete_set.add(int(part))

        # 새로운 라인 리스트 생성 (삭제할 라인 제외)
        new_lines = [line for i, line in enumerate(lines, start=1) if i not in lines_to_delete_set]

        # 출력 파일명 설정 (_lineremove.csv)
        base_name, _ = os.path.splitext(file_path)
        modified_file_path = f"{base_name}_lineremove.csv"

        # 수정된 내용 저장
        with open(modified_file_path, "w", encoding="utf-8") as file:
            file.writelines(new_lines)

        print(f"✅ 삭제 완료! '{modified_file_path}'에 저장되었습니다.")

    except FileNotFoundError:
        print(f"❌ 오류: '{file_path}' 파일을 찾을 수 없습니다.")
    except ValueError:
        print("❌ 오류: 삭제할 라인은 숫자 또는 범위(예: 3-5,7,10)로 입력해야 합니다.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    # 명령줄 인자 파싱
    parser = argparse.ArgumentParser(description="TXT 파일에서 특정 라인을 삭제하고 '_lineremove.csv'로 저장합니다.")
    parser.add_argument("file", help="TXT 파일 경로 (예: data.txt)")
    parser.add_argument("lines", help="삭제할 라인 번호 (단일 또는 범위 입력 가능, 예: 3-5,7,10)")

    args = parser.parse_args()
    delete_lines(args.file, args.lines)
