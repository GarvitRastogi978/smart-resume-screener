# src/parse_resume.py
import pdfplumber
import docx
import re

def extract_text_from_pdf(path):
    text = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text.append(page.extract_text() or "")
    return "\n".join(text)

def extract_text_from_docx(path):
    doc = docx.Document(path)
    paragraphs = [p.text for p in doc.paragraphs]
    return "\n".join(paragraphs)

def extract_text(path):
    path = str(path)
    if path.lower().endswith(".pdf"):
        return extract_text_from_pdf(path)
    elif path.lower().endswith(".docx") or path.lower().endswith(".doc"):
        # python-docx reads .docx; .doc might need textract conversion
        return extract_text_from_docx(path)
    else:
        # fallback: try to read as text
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

def extract_years_of_experience(text):
    """
    Heuristic: look for patterns like 'X years', 'X+ years' or ranges '2018-2023'
    Returns approximate years (int) or None
    """
    text_lower = text.lower()
    # pattern: '(\d+(\.\d+)?)\s*\+?\s*(years?|yrs?)'
    import re
    m = re.search(r'(\d+(?:\.\d+)?)\s*\+?\s*(years|yrs)', text_lower)
    if m:
        try:
            return float(m.group(1))
        except:
            pass
    # fallback: find earliest job year and latest year
    years = re.findall(r'\b(19|20)\d{2}\b', text)
    # years captured with leading two digits, convert properly:
    years_full = re.findall(r'\b(19|20)\d{2}\b', text)
    # simpler approach: find four-digit years
    years4 = re.findall(r'\b(19|20)\d{2}\b', text)
    try:
        years_all = [int(y) for y in re.findall(r'\b(19|20)\d{2}\b', text)]
        if years_all:
            span = max(years_all) - min(years_all)
            return float(span)
    except:
        pass
    return None
