import pytesseract
import cv2
import os
import re
import random

# 各学校/考试类型模板坐标（示例，可根据实际答题卡微调）
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
    优先根据模板 OCR 提取名字，失败则 fallback 用文件名推测
    """
    text = ""

    if template_name and template_name in TEMPLATES:
        img = cv2.imread(image_path)
        if img is None:
            print(f"⚠️ 无法读取图像: {image_path}")
            return fallback_name_from_filename(image_path)

        coords = TEMPLATES[template_name]
        x, y, w, h = coords["x"], coords["y"], coords["w"], coords["h"]
        name_region = img[y:y + h, x:x + w]

        gray = cv2.cvtColor(name_region, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray, lang="eng").strip()
        print(f"🔍 OCR结果（{template_name}）: '{text}'")

    if not text or len(text) < 2:
        text = fallback_name_from_filename(image_path)
        print(f"✅ fallback 名字: {text}")

    return text

def fallback_name_from_filename(image_path):
    """
    fallback 用文件名生成名字
    """
    filename = os.path.splitext(os.path.basename(image_path))[0]

    if "WhatsApp" in filename:
        time_match = re.search(r'(\d{2}\.\d{2}\.\d{2})', filename)
        if time_match:
            time_str = time_match.group(1).replace('.', '')
            return f"学生_{time_str}"
        parts = filename.split('_')
        if len(parts) > 1:
            return f"学生_{parts[-1][:8]}"

    clean = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff]', '_', filename)
    clean = re.sub(r'_+', '_', clean).strip('_')
    return clean[:20] if clean else "Student_Unknown"

def extract_student_answers(image_path, total_questions):
    """
    演示版：随机生成学生答案，后期可替换为真正的 OMR 逻辑
    """
    choices = ['A', 'B', 'C', 'D']
    print(f"📝 生成 {total_questions} 题的学生答案（示例随机）")
    return [random.choice(choices) for _ in range(total_questions)]
