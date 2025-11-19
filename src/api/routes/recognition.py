# api-ocr/src/api/routes/recognition.py

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pdf2image import convert_from_bytes
from src.models.schemas import ImageUploadForOCR
from typing import List, Dict, Any
import logging
import pytesseract
from PIL import Image
import io
import re

router = APIRouter(prefix="/recognition", tags = ["Recognition"])

@router.post("/img-file")
def text_from_img_file(file: UploadFile = File(...)):
    # validação simples
    if file.content_type not in ["image/jpeg", "image/png"]:
        return {"error": "Formato inválido. Use JPEG ou PNG."}

    # leitura da imagem
    image_bytes = file.file.read()
    image = Image.open(io.BytesIO(image_bytes))
    
    # processamento OCR
    texto = pytesseract.image_to_string(image, lang="por")
    
    return {"text": texto}


@router.post("/zip-files")
def text_from_zip_files(file: UploadFile = File(...)):
    # validação simples
    if file.content_type not in ["image/jpeg", "image/png"]:
        return {"error": "Formato inválido. Use JPEG ou PNG."}

    # leitura da imagem
    image_bytes = file.file.read()
    image = Image.open(io.BytesIO(image_bytes))
    
    # processamento OCR
    texto = pytesseract.image_to_string(image, lang="por")
    
    return {"text": texto}

@router.post("/pdf-file")
def text_from_pdf_file(file: UploadFile = File(...)):
    # validação simples
    if file.content_type != "application/pdf":
        return JSONResponse(
            status_code=400,
            content={"error": "O arquivo deve ser um PDF"}
        )

    # leitura do conteúdo do pdf
    pdf_bytes = file.file.read()

    # Converte cada página em imagem
    pages = convert_from_bytes(pdf_bytes)

    results: List[Dict[str, Any]] = []
    for page_number, page in enumerate(pages, start=1):
        # Aplica OCR com Tesseract
        text = pytesseract.image_to_string(page, lang="por")  # 'por' para português
        results.append({
            "page": page_number,
            "text": text.strip()
            })

    return {"ocr_result": results}

