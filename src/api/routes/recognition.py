# api-ocr/src/api/routes/recognition.py

import time
from typing import Literal
from fastapi import APIRouter, File, HTTPException, Query, UploadFile, status
from fastapi.responses import JSONResponse
import logging
from src.services.ocr_service import ocr_image, ocr_pdf
from src.models.schemas import RecognitionImageFileOutput, ALLOWED


router = APIRouter(prefix="/recognition", tags = ["Recognition"])
logger = logging.getLogger(__name__)


@router.post("/image-file", response_model=RecognitionImageFileOutput)
async def text_from_file(file: UploadFile = File(...)):

    # 1. File type validation
    if file.content_type not in ALLOWED:
        logger.warning(
            f"Tentativa de upload inválido: {file.filename}, "
            f"Tipo: {file.content_type}"
        )
        # Retorna HTTP 400 - Bad Request
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de arquivo inválido. Somente {', '.join(ALLOWED)} são permitidos."
        )

    logger.info(
        f"Validação bem sucedida: {file.filename}, "
        f"Size: {(file.size / 1000):.1f}KB"
    )

    # 2. Processing
    try:
        image_bytes = await file.read()
        text = ocr_image(image_bytes, "por")
    except Exception as e:
        logger.error(f"Erro no processamento OCR para {file.filename}: {e}")
        # Retorna um HTTP 500 caso o serviço falhe
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"OCR service failed: {e}"
        )

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
            content={"error": "Formato inválido! O arquivo deve ser um ZIP."},
        )
    # leitura da imagem
    image_bytes = file.file.read()
    # processamento OCR
    texto = ocr_image(image_bytes)
    return {"text": texto}


@router.post("/pdf-file", status_code=200)
def text_from_pdf_file(
    file: UploadFile = File(...),
    lang: Literal["por", "eng", "fra", "spa"] = Query(
        "por", description="Idioma do OCR"
    ),
):
    # validação: nenhum arquivo enviado
    if file is None:
        logger.error(
            "NENHUM ARQUIVO ENVIADO - Nenhum arquivo foi enviado na requisição."
        )
        return JSONResponse(
            status_code=400,
            content={
                "error": "Nenhum arquivo foi enviado. É necessário enviar um PDF."
            },
        )

    # validação do tipo de arquivo
    if file.content_type != "application/pdf":
        logger.error(
            f"TIPO DE ARQUIVO INVÁLIDO | Name={file.filename} | "
            f"Size={file.size/1000:.1f}KB | "
            f"ContentType={file.content_type}"
        )
        return JSONResponse(
            status_code=400,
            content={"error": "Formato inválido! O arquivo deve ser um PDF."},
        )

    # medir tempo de execução
    start_time = time.time()

    # leitura do conteúdo do pdf
    pdf_bytes = file.file.read()

    # processamento OCR
    results = ocr_pdf(pdf_bytes)
    return {"ocr_result": results}