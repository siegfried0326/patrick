#!/usr/bin/env python3
"""
Word 문서에서 이미지를 추출하고 AI 분석 후 엑셀 파일로 생성하는 스크립트
"""

import os
import zipfile
import shutil
from pathlib import Path
import base64
from io import BytesIO

try:
    from PIL import Image
    import openpyxl
    from openpyxl.drawing.image import Image as XLImage
    from openpyxl.styles import Font, Alignment, PatternFill
except ImportError:
    print("필요한 라이브러리를 설치해주세요:")
    print("pip install pillow openpyxl python-docx")
    exit(1)


def extract_images_from_docx(docx_path, output_folder):
    """
    Word 문서(.docx)에서 이미지를 추출합니다.

    Args:
        docx_path: Word 문서 파일 경로
        output_folder: 이미지를 저장할 폴더

    Returns:
        추출된 이미지 파일 경로 리스트
    """
    # 출력 폴더 생성
    os.makedirs(output_folder, exist_ok=True)

    # .docx 파일은 실제로 ZIP 파일입니다
    temp_dir = os.path.join(output_folder, 'temp_extract')
    os.makedirs(temp_dir, exist_ok=True)

    image_files = []

    try:
        # ZIP으로 압축 해제
        with zipfile.ZipFile(docx_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # word/media 폴더에서 이미지 찾기
        media_path = os.path.join(temp_dir, 'word', 'media')

        if os.path.exists(media_path):
            for filename in os.listdir(media_path):
                file_path = os.path.join(media_path, filename)

                # 이미지 파일만 복사
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.wmf', '.emf')):
                    output_path = os.path.join(output_folder, filename)
                    shutil.copy2(file_path, output_path)
                    image_files.append(output_path)
                    print(f"이미지 추출: {filename}")

        # 임시 폴더 삭제
        shutil.rmtree(temp_dir, ignore_errors=True)

    except Exception as e:
        print(f"오류 발생: {e}")
        shutil.rmtree(temp_dir, ignore_errors=True)

    return image_files


def analyze_image(image_path):
    """
    이미지를 분석하여 설명을 생성합니다.
    (실제 AI 분석은 API 키가 필요하므로, 기본 정보만 제공)

    Args:
        image_path: 이미지 파일 경로

    Returns:
        이미지 분석 정보 딕셔너리
    """
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            format_type = img.format
            mode = img.mode

            # 기본 분석 정보
            analysis = {
                '파일명': os.path.basename(image_path),
                '경로': image_path,
                '크기': f"{width} x {height}",
                '포맷': format_type,
                '색상모드': mode,
                '파일크기': f"{os.path.getsize(image_path) / 1024:.2f} KB",
                '설명': f"{format_type} 이미지, 해상도: {width}x{height}",
                '추가정보': '게임기획 문서 내 이미지'
            }

            return analysis

    except Exception as e:
        return {
            '파일명': os.path.basename(image_path),
            '경로': image_path,
            '오류': str(e)
        }


def create_excel_report(image_analyses, output_excel_path):
    """
    이미지 분석 결과를 엑셀 파일로 생성합니다.

    Args:
        image_analyses: 이미지 분석 결과 리스트
        output_excel_path: 생성할 엑셀 파일 경로
    """
    # 새 워크북 생성
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "이미지 분석 결과"

    # 헤더 스타일
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF", size=12)

    # 헤더 작성
    headers = ['번호', '파일명', '크기', '포맷', '색상모드', '파일크기', '설명', '추가정보', '경로']
    for col, header in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', vertical='center')

    # 데이터 작성
    for idx, analysis in enumerate(image_analyses, start=2):
        ws.cell(row=idx, column=1, value=idx-1)  # 번호
        ws.cell(row=idx, column=2, value=analysis.get('파일명', ''))
        ws.cell(row=idx, column=3, value=analysis.get('크기', ''))
        ws.cell(row=idx, column=4, value=analysis.get('포맷', ''))
        ws.cell(row=idx, column=5, value=analysis.get('색상모드', ''))
        ws.cell(row=idx, column=6, value=analysis.get('파일크기', ''))
        ws.cell(row=idx, column=7, value=analysis.get('설명', ''))
        ws.cell(row=idx, column=8, value=analysis.get('추가정보', ''))
        ws.cell(row=idx, column=9, value=analysis.get('경로', ''))

    # 열 너비 자동 조정
    column_widths = {
        'A': 8,   # 번호
        'B': 25,  # 파일명
        'C': 15,  # 크기
        'D': 12,  # 포맷
        'E': 12,  # 색상모드
        'F': 15,  # 파일크기
        'G': 50,  # 설명
        'H': 20,  # 추가정보
        'I': 60   # 경로
    }

    for col, width in column_widths.items():
        ws.column_dimensions[col].width = width

    # 행 높이 설정
    ws.row_dimensions[1].height = 25

    # 엑셀 파일 저장
    wb.save(output_excel_path)
    print(f"\n엑셀 파일 생성 완료: {output_excel_path}")


def main():
    """메인 실행 함수"""
    print("=" * 70)
    print("Word 문서 이미지 추출 및 분석 도구")
    print("=" * 70)

    # 파일 경로 입력 (기본값 설정)
    default_path = r"C:\Users\up_ma\OneDrive\바탕 화면\게임캔버스\1.기획이론\포트폴리오_구본일\원고작업\원고서식_25년버전의 1. 게임기획 취업바이블_기획의개요"

    print(f"\n기본 경로: {default_path}")
    docx_path = input("\nWord 문서 경로를 입력하세요 (엔터: 기본값 사용): ").strip()

    if not docx_path:
        docx_path = default_path

    # 파일 존재 확인
    if not os.path.exists(docx_path):
        print(f"\n오류: 파일을 찾을 수 없습니다: {docx_path}")
        print("\n전체 파일 경로를 확인해주세요.")
        print("예: C:\\Users\\up_ma\\OneDrive\\바탕 화면\\문서.docx")
        return

    # 출력 폴더 설정
    base_name = os.path.splitext(os.path.basename(docx_path))[0]
    output_folder = os.path.join(os.path.dirname(docx_path), f"{base_name}_이미지")

    print(f"\n이미지 저장 폴더: {output_folder}")

    # 이미지 추출
    print("\n" + "=" * 70)
    print("1단계: 이미지 추출 중...")
    print("=" * 70)
    image_files = extract_images_from_docx(docx_path, output_folder)

    if not image_files:
        print("\n이미지를 찾을 수 없습니다.")
        return

    print(f"\n총 {len(image_files)}개의 이미지를 추출했습니다.")

    # 이미지 분석
    print("\n" + "=" * 70)
    print("2단계: 이미지 분석 중...")
    print("=" * 70)
    image_analyses = []
    for img_path in image_files:
        analysis = analyze_image(img_path)
        image_analyses.append(analysis)
        print(f"분석 완료: {analysis.get('파일명', '')}")

    # 엑셀 파일 생성
    print("\n" + "=" * 70)
    print("3단계: 엑셀 파일 생성 중...")
    print("=" * 70)
    excel_path = os.path.join(os.path.dirname(docx_path), f"{base_name}_이미지분석.xlsx")
    create_excel_report(image_analyses, excel_path)

    print("\n" + "=" * 70)
    print("작업 완료!")
    print("=" * 70)
    print(f"\n추출된 이미지: {output_folder}")
    print(f"분석 결과 엑셀: {excel_path}")
    print("\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n작업이 취소되었습니다.")
    except Exception as e:
        print(f"\n오류 발생: {e}")
        import traceback
        traceback.print_exc()

    input("\n엔터를 누르면 종료합니다...")
