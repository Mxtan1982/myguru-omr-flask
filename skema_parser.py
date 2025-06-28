import re
import os
import random
from docx import Document
import fitz  # PyMuPDF

def parse_answers_from_text(text):
    """
    解析类似 '1. A', '2) B' 的格式
    返回按顺序排好的答案列表
    """
    pattern = r"\b(\d+)[\.\)]\s*([ABCD])"
    matches = re.findall(pattern, text, re.IGNORECASE)
    # 排序题号，防止乱序
    sorted_matches = sorted(matches, key=lambda x: int(x[0]))
    answers = [ans.upper() for _, ans in sorted_matches]
    print(f"📋 提取到 {len(answers)} 题答案：{answers}")
    return answers

def extract_from_docx(path):
    """
    从 DOCX 提取文本并解析
    """
    try:
        doc = Document(path)
        full_text = "\n".join([para.text for para in doc.paragraphs])
        print("✅ 读取 DOCX 成功")
        return parse_answers_from_text(full_text)
    except Exception as e:
        print(f"❌ 读取 DOCX 错误: {e}")
        return []

def extract_from_pdf(path):
    """
    从 PDF 提取文本并解析
    """
    try:
        text = ""
        pdf_doc = fitz.open(path)
        for page in pdf_doc:
            text += page.get_text()
        pdf_doc.close()
        print("✅ 读取 PDF 成功")
        return parse_answers_from_text(text)
    except Exception as e:
        print(f"❌ 读取 PDF 错误: {e}")
        return []

def extract_skema(path):
    """
    根据文件扩展名自动选择提取方式：
    - PDF: 用 PyMuPDF
    - DOCX: 用 python-docx
    - 图片: 生成随机示例
    """
    _, ext = os.path.splitext(path.lower())

    if ext == ".pdf":
        return extract_from_pdf(path)
    elif ext == ".docx":
        return extract_from_docx(path)
    elif ext in [".jpg", ".jpeg", ".png"]:
        print("⚠️ 图片暂未集成 OCR，返回 40 题示例答案")
        choices = ['A', 'B', 'C', 'D']
        answers = [random.choice(choices) for _ in range(40)]
        return answers
    else:
        raise ValueError(f"❌ 不支持的文件格式：{ext}，请上传 PDF 或 DOCX")
