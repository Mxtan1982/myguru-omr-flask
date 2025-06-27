import pytesseract
import cv2
import os
import re
import random

# 多模板坐标（含 STPM、华小、SK、SM、SMK、SPM、UPSR、UASA、PT3、SEKOLAH_SENI、SEKOLAH_SUKAN、VOKASIONAL）
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
    优先使用模板区域 OCR 提取名字，如果失败则使用文件名推测
    """
    text = ""

    if template_name and template_name in TEMPLATES:
        img = cv2.imread(image_path)
        coords = TEMPLATES[template_name]
        x, y, w, h = coords["x"], coords["y"], coords["w"], coords["h"]
        name_region = img[y:y + h, x:x + w]

        gray = cv2.cvtColor(name_region, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray, lang="eng").strip()

    # 如果 OCR 失败或没有模板，就 fallback
    if not text or len(text) < 2:
        text = fallback_name_from_filename(image_path)

    return text

def fallback_name_from_filename(image_path):
    """
    使用文件名生成学生名
    """
    filename = os.path.splitext(os.path.basename(image_path))[0]

    if "WhatsApp" in filename:
        time_match = re.search(r'(\d{2}\.\d{2}\.\d{2})', filename)
        if time_match:
            time_str = time_match.group(1).replace('.', '')
            return f"学生_{time_str}"
        else:
            parts = filename.split('_')
            if len(parts) > 1:
                return f"学生_{parts[-1][:8]}"

    clean_name = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff]', '_', filename)
    clean_name = re.sub(r'_+', '_', clean_name).strip('_')

    if clean_name:
        return clean_name[:20]
    else:
        return "Student_Unknown"

def extract_student_answers(image_path, total_questions):
    """
    演示版：随机生成学生答案，可替换为 OMR 识别
    """
    choices = ['A', 'B', 'C', 'D']
    print(f"📝 生成 {total_questions} 题的学生答案 (示例随机)")
    answers = []
    for _ in range(total_questions):
        answers.append(random.choice(choices))
    return answers
