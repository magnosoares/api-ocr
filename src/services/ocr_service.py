import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import io
from typing import List, Dict, Any

def ocr_image(image_bytes: bytes, lang: str = "por") -> str:
    image = Image.open(io.BytesIO(image_bytes))
    return pytesseract.image_to_string(image, lang=lang).strip()

def ocr_pdf(pdf_bytes: bytes, lang: str = "por") -> List[Dict[str, Any]]:
    pages = convert_from_bytes(pdf_bytes)
    results: List[Dict[str, Any]] = []
    for page_number, page in enumerate(pages, start=1):
        text = pytesseract.image_to_string(page, lang=lang).strip()
        results.append({"page": page_number, "text": text})
    return results
