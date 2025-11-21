# src/service/ocr_service.py

import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import io
import re
from typing import List, Dict, Any

def ocr_image(image_bytes: bytes, lang: str = "por") -> str:
    """
    Receives an image and returns the extracted OCR text.
    """

    # receive the raw image
    image = Image.open(io.BytesIO(image_bytes))

    # OCR
    text = pytesseract.image_to_string(image, lang=lang)

    # text cleaning
    text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()

def ocr_pdf(pdf_bytes: bytes, lang: str = "por") -> List[Dict[str, Any]]:
    """
    Receives a pdf file and returns the extracted OCR text.
    """
    # receive the raw file
    pages = convert_from_bytes(pdf_bytes)
    
    results: List[Dict[str, Any]] = []
    for page_number, page in enumerate(pages, start=1):
        text = pytesseract.image_to_string(page, lang=lang).strip()
        results.append({"page": page_number, "text": text})
    return results