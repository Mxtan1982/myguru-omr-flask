import re
from docx import Document
import fitz
import os
import random

def parse_answers_from_text(text):
    pattern = r"\b(\d+)[\.\)]\s*([ABCD])"
    matches = re.findall(pattern, text)
    sorted_matches = sorted(matches, key=lambda x: int(x[0]))
    return [ans for _, ans in sorted_matches]

def extract_from_docx(path):
    doc = Document(path)
    text = "\n".join([p.text for p in doc.paragraphs])
    return parse_answers_from_text(text)

def extract_from_pdf(path):
    text = ""
    with fitz.open(path) as doc:
        for page in doc:
            text += page.get_text()
    return parse_answers_from_text(text)

def extract_skema(path):
    if path.lower().endswith(".pdf"):
        return extract_from_pdf(path)
    elif path.lower().endswith(".docx"):
        return extract_from_docx(path)
    else:
        choices = ['A', 'B', 'C', 'D']
        return [random.choice(choices) for _ in range(40)]
