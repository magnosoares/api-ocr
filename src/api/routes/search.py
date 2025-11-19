# api-ocr/src/api/routes/search.py

from fastapi import APIRouter, File, HTTPException, UploadFile
#from src.models.schemas import ImageUploadForOCR
import logging
import pytesseract
from PIL import Image
import io
import re

router = APIRouter(prefix="/search", tags = ["Search"])

@router.post("/file")
def text_from_file(file: UploadFile = File(...)):
    # validação simples
    if file.content_type not in ["image/jpeg", "image/png"]:
        return {"error": "Formato inválido. Use JPEG ou PNG."}

    # leitura da imagem
    image_bytes = file.file.read()
    image = Image.open(io.BytesIO(image_bytes))
    
    # processamento OCR
    texto = pytesseract.image_to_string(image, lang="por")
    texto = re.sub(r"\s+", " ", texto.replace("\n", " ").replace("\r", " ").replace("\t", " "))
    
    return {"text": texto}


@router.post("/zip-files")
def text_from_file(file: UploadFile = File(...)):
    # validação simples
    if file.content_type not in ["image/jpeg", "image/png"]:
        return {"error": "Formato inválido. Use JPEG ou PNG."}

    # leitura da imagem
    image_bytes = file.file.read()
    image = Image.open(io.BytesIO(image_bytes))
    
    # processamento OCR
    texto = pytesseract.image_to_string(image, lang="por")
    texto = re.sub(r"\s+", " ", texto.replace("\n", " ").replace("\r", " ").replace("\t", " "))
    
    return {"text": texto}