# api-ocr/src/api/routes/recognition.py

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
import logging
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import pytesseract
from PIL import Image
import io
import re
from src.services.ocr_service import ocr_image, ocr_pdf
from src.models.schemas import RecognitionImageFileInput, RecognitionImageFileOutput

router = APIRouter(prefix="/recognition", tags = ["Recognition"])

logger = logging.getLogger(__name__)


@router.post("/image-file", response_model=RecognitionImageFileOutput)
async def text_from_file(input: RecognitionImageFileInput = Depends()):

    file = input.file

    logger.info(
        f"Validação bem sucedida: {file.filename}, "
        f"Size: {(file.size / 1000):.1f}KB"
    )

    image_bytes = await file.read()
    text = ocr_image(image_bytes, "por")

    return RecognitionImageFileOutput(
        file_name=file.filename,
        file_size=file.size,
        text_output=text
    )



@router.post("/zip-files")
def text_from_zipfile(file: UploadFile = File(...)):
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


@router.post("/pdf-file", status_code = 200)
def text_from_pdf_file(file: UploadFile = File(...)):
    # validação simples
    if file.content_type != "application/pdf":
        logger.warning(f"FILE INFO - Name: {file.filename}, Size: {(file.size / 1000):.1f}KB")
        return JSONResponse(
            status_code=400,
            content={"error": "Formato inválido! O arquivo deve ser um PDF."}
        )
    
    logger.info(f"FILE INFO - Name: {file.filename}, Size: {(file.size / 1000):.1f}KB")

    # leitura do conteúdo do pdf
    pdf_bytes = file.file.read()

    # processamento OCR
    results = ocr_pdf(pdf_bytes)
    return {"ocr_result": results}