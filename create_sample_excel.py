#!/usr/bin/env python3
"""
샘플 엑셀 파일 생성 스크립트
"""

import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill

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

# 샘플 데이터
sample_data = [
    {
        '번호': 1,
        '파일명': 'image1.png',
        '크기': '1920 x 1080',
        '포맷': 'PNG',
        '색상모드': 'RGB',
        '파일크기': '245.78 KB',
        '설명': 'PNG 이미지, 해상도: 1920x1080 - 게임 UI 디자인',
        '추가정보': '게임기획 문서 내 이미지',
        '경로': 'C:\\Users\\up_ma\\OneDrive\\바탕 화면\\게임캔버스\\1.기획이론\\포트폴리오_구본일\\원고작업\\원고서식_25년버전\\1. 게임기획 취업바이블_기획의개요_이미지\\image1.png'
    },
    {
        '번호': 2,
        '파일명': 'image2.jpg',
        '크기': '1280 x 720',
        '포맷': 'JPEG',
        '색상모드': 'RGB',
        '파일크기': '156.32 KB',
        '설명': 'JPEG 이미지, 해상도: 1280x720 - 캐릭터 컨셉 아트',
        '추가정보': '게임기획 문서 내 이미지',
        '경로': 'C:\\Users\\up_ma\\OneDrive\\바탕 화면\\게임캔버스\\1.기획이론\\포트폴리오_구본일\\원고작업\\원고서식_25년버전\\1. 게임기획 취업바이블_기획의개요_이미지\\image2.jpg'
    },
    {
        '번호': 3,
        '파일명': 'diagram1.png',
        '크기': '800 x 600',
        '포맷': 'PNG',
        '색상모드': 'RGB',
        '파일크기': '89.54 KB',
        '설명': 'PNG 이미지, 해상도: 800x600 - 게임 플로우 다이어그램',
        '추가정보': '게임기획 문서 내 이미지',
        '경로': 'C:\\Users\\up_ma\\OneDrive\\바탕 화면\\게임캔버스\\1.기획이론\\포트폴리오_구본일\\원고작업\\원고서식_25년버전\\1. 게임기획 취업바이블_기획의개요_이미지\\diagram1.png'
    },
    {
        '번호': 4,
        '파일명': 'screenshot1.png',
        '크기': '1366 x 768',
        '포맷': 'PNG',
        '색상모드': 'RGB',
        '파일크기': '198.67 KB',
        '설명': 'PNG 이미지, 해상도: 1366x768 - 게임 스크린샷',
        '추가정보': '게임기획 문서 내 이미지',
        '경로': 'C:\\Users\\up_ma\\OneDrive\\바탕 화면\\게임캔버스\\1.기획이론\\포트폴리오_구본일\\원고작업\\원고서식_25년버전\\1. 게임기획 취업바이블_기획의개요_이미지\\screenshot1.png'
    },
    {
        '번호': 5,
        '파일명': 'logo.png',
        '크기': '512 x 512',
        '포맷': 'PNG',
        '색상모드': 'RGBA',
        '파일크기': '45.23 KB',
        '설명': 'PNG 이미지, 해상도: 512x512 - 게임 로고',
        '추가정보': '게임기획 문서 내 이미지',
        '경로': 'C:\\Users\\up_ma\\OneDrive\\바탕 화면\\게임캔버스\\1.기획이론\\포트폴리오_구본일\\원고작업\\원고서식_25년버전\\1. 게임기획 취업바이블_기획의개요_이미지\\logo.png'
    }
]

# 데이터 작성
for idx, data in enumerate(sample_data, start=2):
    ws.cell(row=idx, column=1, value=data['번호'])
    ws.cell(row=idx, column=2, value=data['파일명'])
    ws.cell(row=idx, column=3, value=data['크기'])
    ws.cell(row=idx, column=4, value=data['포맷'])
    ws.cell(row=idx, column=5, value=data['색상모드'])
    ws.cell(row=idx, column=6, value=data['파일크기'])
    ws.cell(row=idx, column=7, value=data['설명'])
    ws.cell(row=idx, column=8, value=data['추가정보'])
    ws.cell(row=idx, column=9, value=data['경로'])

# 열 너비 자동 조정
column_widths = {
    'A': 8,   # 번호
    'B': 25,  # 파일명
    'C': 15,  # 크기
    'D': 12,  # 포맷
    'E': 12,  # 색상모드
    'F': 15,  # 파일크기
    'G': 60,  # 설명
    'H': 25,  # 추가정보
    'I': 100  # 경로
}

for col, width in column_widths.items():
    ws.column_dimensions[col].width = width

# 행 높이 설정
ws.row_dimensions[1].height = 25

# 데이터 행 높이
for row in range(2, len(sample_data) + 2):
    ws.row_dimensions[row].height = 30

# 엑셀 파일 저장
output_file = "샘플_이미지분석결과.xlsx"
wb.save(output_file)
print(f"샘플 엑셀 파일 생성 완료: {output_file}")
