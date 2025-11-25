# src/service/ocr_service.py

import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import io
import re
from typing import List, Dict, Any
from src.models.schemas import OCRResult


def ocr_image(image_bytes: bytes, lang: str = "por") -> str:
    """
    Receives an image and returns the extracted OCR text.
    """

    # receive the raw image
    image = Image.open(io.BytesIO(image_bytes))

    # OCR
    text = pytesseract.image_to_string(image, lang=lang)

    # text cleaning
    # text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    # text = re.sub(r"\s+", " ", text)

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


def ocr_pdf_texto(pdf_bytes: bytes, lang: str = "por") -> str:
    """
    Receives a pdf file and returns the extracted OCR text.
    """
    # receive the raw file
    pages = convert_from_bytes(pdf_bytes)
    text = ""
    for page_number, page in enumerate(pages, start=1):
        text += pytesseract.image_to_string(page, lang=lang).strip()

    return text.strip()


def pesquisar_texto(texto: str, termo: str, nome_arquivo: str) -> List[Dict[str, Any]]:
    # Busca com regex (case insensitive)
    matches = list(re.finditer(re.escape(termo), texto, re.IGNORECASE))
    trechos = []

    for m in matches:
        inicio = max(0, m.start() - 25)
        fim = min(len(texto), m.end() + 25)
        trecho = texto[inicio:fim].replace("\n", " ").strip()
        trechos.append(f"...{trecho}...")

    return OCRResult(
        arquivo=nome_arquivo, ocorrencias=len(matches), trechos=trechos, texto_ocr=texto
    )
