import pytesseract
import cv2
import os
import re
import random

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
    text = ""
    if template_name and template_name in TEMPLATES:
        img = cv2.imread(image_path)
        coords = TEMPLATES[template_name]
        x, y, w, h = coords["x"], coords["y"], coords["w"], coords["h"]
        name_region = img[y:y + h, x:x + w]
        gray = cv2.cvtColor(name_region, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray, lang="eng").strip()

    if not text:
        text = fallback_name_from_filename(image_path)
    return text

def fallback_name_from_filename(image_path):
    filename = os.path.splitext(os.path.basename(image_path))[0]
    time_match = re.search(r'(\d{2}\.\d{2}\.\d{2})', filename)
    if time_match:
        return f"学生_{time_match.group(1).replace('.', '')}"
    return filename

def extract_student_answers(image_path, total_questions):
    choices = ['A', 'B', 'C', 'D']
    return [random.choice(choices) for _ in range(total_questions)]
