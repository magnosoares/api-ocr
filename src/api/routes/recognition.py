# api-ocr/src/api/routes/recognition.py

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from src.services.ocr_service import ocr_image, ocr_pdf
from src.models.schemas import ImageUploadForOCR
from typing import List, Dict, Any
import logging
from PIL import Image
import io
import re

router = APIRouter(prefix="/recognition", tags = ["Recognition"])

@router.post("/img-file")
def text_from_img_file(file: UploadFile = File(...)):
    # validação simples
    if file.content_type not in ["image/jpeg", "image/png"]:
        return JSONResponse(
            status_code=400,
            content={"error": "Formato inválido! Use JPEG ou PNG."}
        )
    # leitura da imagem
    image_bytes = file.file.read()
    # processamento OCR
    texto = ocr_image(image_bytes)
    return {"text": texto}


@router.post("/zip-files")
def text_from_zip_files(file: UploadFile = File(...)):
    # validação simples
    if file.content_type not in ["image/jpeg", "image/png"]:
        return JSONResponse(
            status_code=400,
            content={"error": "Formato inválido! O arquivo deve ser um ZIP."}
        )
    # leitura da imagem
    image_bytes = file.file.read()
    # processamento OCR
    texto = ocr_image(image_bytes)
    return {"text": texto}

@router.post("/pdf-file")
def text_from_pdf_file(file: UploadFile = File(...)):
    # validação simples
    if file.content_type != "application/pdf":
        return JSONResponse(
            status_code=400,
            content={"error": "Formato inválido! O arquivo deve ser um PDF."}
        )
    # leitura do conteúdo do pdf
    pdf_bytes = file.file.read()
    # processamento OCR
    results = ocr_pdf(pdf_bytes)
    return {"ocr_result": results}

