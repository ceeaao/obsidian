# pip3 install --break-system-packages Pillow

import subprocess
import os
import sys
from PIL import Image, ImageDraw, ImageFont
import shutil

def extract_frames(video_path, output_folder, frame_count=30):
    # 비디오의 총 길이를 가져옵니다.
    result = subprocess.run(['ffmpeg', '-i', video_path, '-hide_banner'], stderr=subprocess.PIPE, text=True)
    duration_line = [x for x in result.stderr.split('\n') if "Duration" in x][0]
    duration_str = duration_line.split(",")[0].split("Duration:")[1].strip()
    h, m, s = map(float, duration_str.split(':'))
    total_seconds = h * 3600 + m * 60 + s

    # 각 구간 계산
    interval = total_seconds / frame_count
    
    # 폴더 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    timestamps = []
    # 각 구간에서 이미지 추출
    for i in range(frame_count):
        timestamp = i * interval
        timestamps.append(timestamp)
        output_image_path = os.path.join(output_folder, f"frame_{i+1}.jpg")
        subprocess.run([
            'ffmpeg', '-ss', str(timestamp), '-i', video_path, '-frames:v', '1',
            output_image_path, '-hide_banner'
        ])
    return timestamps

def format_timestamp(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02}:{m:02}:{s:02}"

def create_thumbnail_image(images_folder, output_image_path, timestamps, images_per_row=5):
    images = [Image.open(os.path.join(images_folder, img)) for img in sorted(os.listdir(images_folder)) if img.endswith('.jpg')]
    widths, heights = zip(*(i.size for i in images))

    # 텍스트 폰트 설정
    # 텍스트 폰트 설정
    font_path = "/System/Library/Fonts/AppleSDGothicNeo.ttc"  # 폰트 경로를 시스템에 맞게 수정하세요
    try:
        font = ImageFont.truetype(font_path, 150)  # 폰트와 크기 설정
    except IOError:
        font = ImageFont.load_default()  # 기본 폰트 사용
        print("Custom font load failed, using default font.")

    # 텍스트 높이 계산
    text_height = font.getbbox("Test")[3] + 10  # 문자열 'Test'의 높이를 계산

    # 최대 너비와 총 높이를 계산
    max_width = max(widths)
    #max_height = max(heights) + text_height  # 텍스트 높이 추가
    max_height = max(heights)
    total_width = max_width * images_per_row
    total_height = max_height * ((len(images) + images_per_row - 1) // images_per_row)

    # 새 이미지 생성
    new_im = Image.new('RGB', (total_width, total_height))
    draw = ImageDraw.Draw(new_im)

    # 이미지 병합 및 텍스트 추가
    x_offset = 0
    y_offset = 0
    for i, (im, timestamp) in enumerate(zip(images, timestamps)):
        #new_im.paste(im, (x_offset, y_offset + text_height))
        new_im.paste(im, (x_offset, y_offset))
        time_str = format_timestamp(timestamp)

        #text_width = font.getbbox(time_str)[2]  # 텍스트의 실제 너비를 계산
        #text_background_area = [x_offset + 5, y_offset, x_offset + 5 + text_width, y_offset + text_height]
        #draw.rectangle(text_background_area, fill='yellow')  # 노란색 배경 추가
        #draw.text((x_offset + 5, y_offset), time_str, font=font, fill='black')  # 위치 조정

        text_bbox = font.getbbox(time_str)  # 텍스트 바운딩 박스 계산
        text_width = text_bbox[2] - text_bbox[0]  # 텍스트 너비
        text_height = text_bbox[3] - text_bbox[1] + 50  # 텍스트 높이
        text_x = x_offset + (max_width - text_width) // 2  # 가운데 정렬
        text_y = y_offset  # 최상단에 텍스트
        text_background_area = [text_x, text_y, text_x + text_width, text_y + text_height]
        draw.rectangle(text_background_area, fill='gray')  # 노란색 배경 추가
        draw.text((text_x, text_y), time_str, font=font, fill='black')  # 검은색 텍스트 추가

        
        x_offset += max_width
        if (i + 1) % images_per_row == 0:
            x_offset = 0
            y_offset += max_height

    new_im.save(output_image_path, 'JPEG')

# CLI를 통한 입력 처리
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <video_path>")
        sys.exit(1)

    video_path = sys.argv[1]
    base_filename = os.path.splitext(os.path.basename(video_path))[0]
    output_folder = 'frames'
    output_image_path = f'{base_filename}_thumbnail.jpg'

    timestamps = extract_frames(video_path, output_folder)
    create_thumbnail_image(output_folder, output_image_path, timestamps)

    print(f'Thumbnail created: {output_image_path}')

    # 임시 폴더 삭제
    shutil.rmtree(output_folder)
    print(f"Temporary folder '{output_folder}' has been deleted.")
