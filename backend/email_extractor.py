import re
from backend.pdf_reader import extract_text
from docx import Document
def extract_emails(file_path):
    text=""
    if file_path.endswith(".pdf"):
        text=extract_text(file_path)
    elif file_path.endswith(".docx"):
        doc=Document(file_path)
        for para in doc.paragraphs:
            text+=para.text+"\n"
    else:
        return []
    emails=re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )
    return list(set(emails))