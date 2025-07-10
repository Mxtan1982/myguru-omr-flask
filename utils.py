import os
import re
import random
import cv2
import easyocr

# ✅ 初始化 EasyOCR Reader（只加载一次）
reader = easyocr.Reader(['en', 'ch_sim'])

# ✅ 每个学校/考试的名字区域模板（坐标要根据你答题卡实际调整）
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


def extract_student_name(image_path, template_name="SJKC"):
    """
    用 EasyOCR 从图片中识别学生名字
    如果失败则 fallback 用文件名推测
    """
    text = ""

    if template_name in TEMPLATES:
        try:
            img = cv2.imread(image_path)
            coords = TEMPLATES[template_name]
            x, y, w, h = coords["x"], coords["y"], coords["w"], coords["h"]

            # 裁剪名字区域
            name_region = img[y:y + h, x:x + w]

            # 灰度处理
            gray = cv2.cvtColor(name_region, cv2.COLOR_BGR2GRAY)

            # OCR 识别
            results = reader.readtext(gray, detail=0)
            text = "".join(results).strip()

            if text:
                print(f"✅ EasyOCR 识别结果: {text}")
        except Exception as e:
            print(f"⚠️ EasyOCR 出错: {e}")

    # 如果没识别到，使用 fallback
    if not text or len(text) < 2:
        text = fallback_name_from_filename(image_path)
        print(f"✅ 使用文件名推测: {text}")

    return text


def fallback_name_from_filename(image_path):
    """
    如果 OCR 失败，就用文件名做名字
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
    OMR 主体：这里留示例，后续可以替换为真实检测逻辑
    """
    choices = ['A', 'B', 'C', 'D']
    print(f"📝 生成 {total_questions} 题答案（示例随机）")
    return [random.choice(choices) for _ in range(total_questions)]
