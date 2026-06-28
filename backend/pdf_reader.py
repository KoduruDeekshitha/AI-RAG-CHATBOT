import fitz
from docx import Document
def extract_text(file_path):
    text=""
    if file_path.lower().endswith(".pdf"):
        doc=fitz.open(file_path)
        for page in doc:
            page_text=page.get_text()
            if page_text:
                text+=page.get_text()
        doc.close()
        return text
    elif file_path.lower().endswith(".docx"):
        doc=Document(file_path)
        text=""
        for para in doc.paragraphs:
            if para.text.strip():
                text+=para.text+"\n"
        return text
    else:
        raise ValueError("Unsupported file format")