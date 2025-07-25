from PIL import Image
import pytesseract
import fitz  # PyMuPDF

def extract_text_per_page(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []

    for i, page in enumerate(doc):
        try:
            text = page.get_text().strip()
            # Fall back if empty or nonsense
            if len(text) < 30 or not re.search(r'[a-zA-Z]{4,}', text):
                raise ValueError("Weak text")
        except:
            # OCR fallback
            pix = page.get_pixmap(dpi=300)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text = pytesseract.image_to_string(img)

        # Hard filter: skip pages full of garbage characters
        if sum(c in text for c in '\u0001\u0007\b\u000e\u0010\u0012') > 10:
            continue
        if len(re.findall(r'[a-zA-Z]', text)) < 20:
            continue

        pages.append((i + 1, text))
    return pages

