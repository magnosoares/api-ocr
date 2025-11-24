# api-ocr/src/api/routes/recognition.py

from fastapi import APIRouter, File, UploadFile, Query
import logging
from fastapi.responses import JSONResponse
from typing import Literal
import time
from src.services.ocr_service import ocr_image, ocr_pdf
from src.models.schemas import RecognitionFileOutput

router = APIRouter(prefix="/recognition", tags=["Recognition"])

logger = logging.getLogger(__name__)


@router.post("/image-file", response_model=RecognitionFileOutput, status_code=200)
def text_from_file(file: UploadFile = File(...)):
    # validação simples
    if file.content_type not in ["image/jpeg", "image/png"]:
        logger.warning(
            f"FILE INFO - Name: {file.filename}, Size: {(file.size / 1000):.1f}KB"
        )
        return {"error": "Formato inválido. Use JPEG ou PNG."}

    logger.info(f"FILE INFO - Name: {file.filename}, Size: {(file.size / 1000):.1f}KB")

    image_bytes = file.file.read()

    text = ocr_image(image_bytes, "por")

    logger.info("Reconhecimento de caracteres finalizado")

    # return {"text": texto}
    return RecognitionFileOutput(
        file_name=file.filename, file_size=file.size, text_output=text
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

    results = ocr_pdf(pdf_bytes, lang=lang)
    elapsed_time = time.time() - start_time

    # concatenar textos das páginas com 5 quebras de linha
    full_text = ("\n\n\n\n\n").join([page["text"] for page in results])

    # logar tempo de OCR
    logger.info(
        f"OCR EXECUTADO COM SUCESSO | Name={file.filename} | "
        f"Size={file.size/1000:.1f}KB | "
        f"Pages={len(results)} | "
        f"Lang={lang} | "
        f"Time={elapsed_time:.2f}s"
    )

    return RecognitionFileOutput(
        file_name=file.filename, file_size=file.size, text_output=full_text
    )
