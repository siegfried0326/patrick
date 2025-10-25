#!/usr/bin/env python3
"""
PDF 파일에서 이미지를 추출하는 스크립트
"""

import os
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
    from PIL import Image
except ImportError:
    print("필요한 라이브러리를 설치해주세요:")
    print("pip install PyMuPDF Pillow")
    input("\n엔터를 누르면 종료합니다...")
    sys.exit(1)


def extract_images_from_pdf(pdf_path, output_folder):
    """
    PDF 파일에서 모든 이미지를 추출합니다.

    Args:
        pdf_path: PDF 파일 경로
        output_folder: 이미지를 저장할 폴더

    Returns:
        추출된 이미지 파일 경로 리스트
    """
    # 출력 폴더 생성
    os.makedirs(output_folder, exist_ok=True)

    # PDF 열기
    pdf_document = fitz.open(pdf_path)

    image_list = []
    image_count = 0

    print(f"\n총 {len(pdf_document)} 페이지를 검사합니다...\n")

    # 각 페이지를 순회
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]

        # 페이지의 이미지 목록 가져오기
        image_list_on_page = page.get_images(full=True)

        print(f"페이지 {page_num + 1}: {len(image_list_on_page)}개의 이미지 발견")

        # 각 이미지 추출
        for img_index, img in enumerate(image_list_on_page):
            xref = img[0]

            try:
                # 이미지 데이터 추출
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                # 파일명 생성
                image_filename = f"page{page_num + 1:03d}_img{img_index + 1:03d}.{image_ext}"
                image_path = os.path.join(output_folder, image_filename)

                # 이미지 저장
                with open(image_path, "wb") as image_file:
                    image_file.write(image_bytes)

                image_list.append(image_path)
                image_count += 1

                print(f"  ✓ 저장: {image_filename} ({len(image_bytes) / 1024:.2f} KB)")

            except Exception as e:
                print(f"  ✗ 오류 (이미지 {img_index + 1}): {e}")

    pdf_document.close()

    print(f"\n" + "=" * 70)
    print(f"총 {image_count}개의 이미지를 추출했습니다!")
    print(f"저장 위치: {output_folder}")
    print("=" * 70)

    return image_list


def main():
    """메인 실행 함수"""
    print("=" * 70)
    print("PDF 이미지 추출 도구")
    print("=" * 70)

    # 기본 경로 설정
    default_pdf = r"C:\Users\up_ma\OneDrive\문서\1. 게임기획 취업바이블_기획의개요.pdf"

    print(f"\n기본 PDF 경로: {default_pdf}")
    pdf_path = input("\nPDF 파일 경로를 입력하세요 (엔터: 기본값 사용): ").strip()

    if not pdf_path:
        pdf_path = default_pdf

    # 파일 존재 확인
    if not os.path.exists(pdf_path):
        print(f"\n오류: PDF 파일을 찾을 수 없습니다: {pdf_path}")
        print("\n전체 파일 경로를 확인해주세요.")
        input("\n엔터를 누르면 종료합니다...")
        return

    # 출력 폴더 설정
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_folder = os.path.join(os.path.dirname(pdf_path), f"{base_name}_추출이미지")

    print(f"\n이미지 저장 폴더: {output_folder}")

    try:
        # 이미지 추출
        print("\n" + "=" * 70)
        print("이미지 추출 시작...")
        print("=" * 70)

        image_files = extract_images_from_pdf(pdf_path, output_folder)

        if not image_files:
            print("\nPDF에서 이미지를 찾을 수 없습니다.")
        else:
            print(f"\n추출 완료! 총 {len(image_files)}개의 이미지가 저장되었습니다.")
            print(f"\n폴더 위치: {output_folder}")

    except Exception as e:
        print(f"\n오류 발생: {e}")
        import traceback
        traceback.print_exc()


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
