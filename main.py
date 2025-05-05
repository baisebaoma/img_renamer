from PIL import Image
import pytesseract
import os
import re

input_dir = 'input_images'
output_dir = 'converted_png'
os.makedirs(output_dir, exist_ok=True)

# 提取课程号
def extract_course_code(text):
    pattern = r'\b(?:CS|ISYE|MGT|ECE|BMED|CSE|PHYS|MATH|AE|CEE|ME|GT)[A-Z0-9]{4,8}\b'
    matches = re.findall(pattern, text)
    return matches[0] if matches else None

# 灰度 + 二值化
def preprocess_image(img):
    gray = img.convert("L")
    binary = gray.point(lambda x: 0 if x < 160 else 255, '1')
    return binary

# 裁剪图像上 1/3 区域
def crop_upper(img):
    w, h = img.size
    return img.crop((0, 0, w, int(h * 0.33)))

# 主识别逻辑
def try_ocr(img):
    processed = preprocess_image(img)
    text = pytesseract.image_to_string(processed, lang='eng')
    return text

# 扫描并处理图片
total_images = 0
success_count = 0
fail_count = 0
unknown_counter = 1

for filename in sorted(os.listdir(input_dir)):
    if filename.lower().endswith(".jpg"):
        total_images += 1
        path = os.path.join(input_dir, filename)
        try:
            with Image.open(path) as img:
                print(f"\n[INFO] Processing {filename}")

                # 第一次识别：全图
                text = try_ocr(img)
                code = extract_course_code(text)
                print(f"[OCR-1] Text: {text.strip()}")

                # 第二次识别：裁剪区域（如果第一次失败）
                if not code:
                    cropped = crop_upper(img)
                    text2 = try_ocr(cropped)
                    code = extract_course_code(text2)
                    print(f"[OCR-2] Cropped Text: {text2.strip()}")

                # 命名逻辑
                if code:
                    png_filename = f"{code}.png"
                    success_count += 1
                    print(f"[✓] Extracted course code: {code}")
                else:
                    png_filename = f"unknown_{unknown_counter:02}.png"
                    unknown_counter += 1
                    fail_count += 1
                    print(f"[✗] Failed to extract course code")

                img.save(os.path.join(output_dir, png_filename), "PNG")
                print(f"[SAVED] {png_filename}")
        except Exception as e:
            print(f"[ERROR] Failed to process {filename}: {e}")
            fail_count += 1

# 总结
print("\n" + "=" * 40)
print(f"Total images processed: {total_images}")
print(f"Successfully named     : {success_count}")
print(f"Failed (used unknown) : {fail_count}")
print("=" * 40)
