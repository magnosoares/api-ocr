# src/service/ocr_service.py

import pytesseract
from PIL import Image
import io
import re

def extract_text_from_image(image_bytes: bytes, lang: str = "por") -> str:
    """
    Receives image bytes and returns the extracted OCR text.
    """

    # receive the raw image
    image = Image.open(io.BytesIO(image_bytes))

    # OCR
    text = pytesseract.image_to_string(image, lang=lang)

    # text cleaning
    text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()