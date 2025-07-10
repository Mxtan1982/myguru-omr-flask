import pytesseract
import cv2
import os
import re
import random

# 多模板区域配置
TEMPLATES = {
    "SJKC": {"x": 50, "y": 50, "w": 400, "h": 100},
    "SK": {"x": 70, "y": 50, "w": 400, "h": 90},
    "SM": {"x": 80, "y": 50, "w": 420, "h": 100},
    "SMK": {"x": 80, "y": 60, "w": 500, "h": 120},
    "SPM": {"x": 100, "y": 40, "w": 450, "h": 110},
    "STPM": {"x": 105, "y": 45, "w": 460, "h": 115},
    "UPSR": {"x": 60, "y": 50, "w": 400, "h": 90},
    "UASA": {"x": 70, "y": 55, "w": 420, "h": 95},
    "PT3": {"x": 90, "y": 45, "w": 480, "h": 100},
    "SEKOLAH_SENI": {"x": 85, "y": 50, "w": 420, "h": 100},
    "SEKOLAH_SUKAN": {"x": 90, "y": 50, "w": 430, "h": 105},
    "VOKASIONAL": {"x": 95, "y": 50, "w": 450, "h": 110}
}

def extract_student_name(image_path, template_name=None):
    """
    根据模板区域使用 pytesseract 提取学生名字
    template_name: 学校或考试代号，如 SJKC, SMK, UPSR 等
    """
    text = ""

    if template_name and template_name in TEMPLATES:
        try:
            img = cv2.imread(image_path)
            coords = TEMPLATES[template_name]
            x, y, w, h = coords["x"], coords["y"], coords["w"], coords["h"]

            # 裁剪名字区域
            name_region = img[y:y + h, x:x + w]

            # 灰度化并 OCR
            gray = cv2.cvtColor(name_region, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray, lang="eng").strip()

            if text:
                print(f"✅ OCR 识别到名字：{text}")
        except Exception as e:
            print(f"⚠️ OCR 出错：{e}")

    if not text or len(text) < 2:
        text = fallback_name_from_filename(image_path)
        print(f"✅ 使用文件名推测：{text}")

    return text

def fallback_name_from_filename(image_path):
    """
    当 OCR 无法识别时，使用文件名生成一个合适的学生名字
    """
    filename = os.path.splitext(os.path.basename(image_path))[0]

    if "WhatsApp" in filename:
        time_match = re.search(r'(\d{2}\.\d{2}\.\d{2})', filename)
        if time_match:
            return f"学生_{time_match.group(1).replace('.', '')}"
        parts = filename.split('_')
        if len(parts) > 1:
            return f"学生_{parts[-1][:8]}"

    clean_name = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff]', '_', filename)
    clean_name = re.sub(r'_+', '_', clean_name).strip('_')

    return clean_name[:20] if clean_name else "Student_Unknown"

def extract_student_answers(image_path, total_questions):
    """
    生成随机答案（示例）
    """
    print(f"📝 生成 {total_questions} 题的学生答案（示例随机）")
    choices = ['A', 'B', 'C', 'D']
    return [random.choice(choices) for _ in range(total_questions)]
