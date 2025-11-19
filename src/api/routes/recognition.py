# api-ocr/src/api/routes/recognition.py

from fastapi import APIRouter, File, HTTPException, UploadFile
from src.models.schemas import ImageUploadForOCR
import logging
import pytesseract
from PIL import Image
import io
import re
from src.services.ocr_service import extract_text_from_image

router = APIRouter(prefix="/recognition", tags = ["Recognition"])

logger = logging.getLogger(__name__)

@router.post("/file")
def text_from_file(file: UploadFile = File(...)):
    # validação simples
    if file.content_type not in ["image/jpeg", "image/png"]:
        logger.warning(f"FILE INFO - Name: {file.filename}, Size: {(file.size / 1000):.1f}KB")
        return {"error": "Formato inválido. Use JPEG ou PNG."}
    
    logger.info(f"FILE INFO - Name: {file.filename}, Size: {(file.size / 1000):.1f}KB")
    image_bytes = file.file.read()
    
    texto = extract_text_from_image(image_bytes, "por")

    logger.info("Reconhecimento de caracteres finalizado")
    
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