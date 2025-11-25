# api-ocr/src/api/routes/recognition.py

import time
import zipfile
import os
import tempfile
from pathlib import Path
from typing import Literal
from fastapi import APIRouter, File, HTTPException, Query, UploadFile, status
from fastapi.responses import JSONResponse
import logging
from src.services.ocr_service import ocr_image, ocr_pdf
from src.models.schemas import (
    RecognitionImageFileOutput,
    RecognitionPDFFileOutput,
    ALLOWED,
    ZipExtractionResponse,
)


router = APIRouter(prefix="/recognition", tags=["Recognition"])
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
            detail=f"Tipo de arquivo inválido. Somente {', '.join(ALLOWED)} são permitidos.",
        )

    logger.info(
        f"Validação bem sucedida: {file.filename}, " f"Size: {(file.size / 1000):.1f}KB"
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
            detail=f"OCR service failed: {e}",
        )

    return RecognitionImageFileOutput(
        file_name=file.filename, file_size=file.size, text_output=text
    )


@router.post("/zip-files", response_model=ZipExtractionResponse, status_code=200)
def text_from_zipfile(file: UploadFile = File(..., media_type="application/zip")):

    # validação simples
    if file.content_type not in ["application/zip", "application/x-zip-compressed"]:
        logger.warning(
            f"ARQUIVO {file.filename} INVÁLIDO! Arquivo deve ser .ZIP"
            f"ContentType = {file.content_type}"
        )
        return JSONResponse(
            status_code=400,
            content={"error": "Formato inválido! O arquivo deve ser um ZIP."},
        )

    # Diretório temporário para extração
    temp_dir = tempfile.mkdtemp()

    zip_path = os.path.join(temp_dir, file.filename)

    with open(zip_path, "wb") as f:
        f.write(file.file.read())

    resultados = []
    arquivos_extraidos = []
    arquivos_rejeitados = []

    try:

        # Extrai os arquivos e salva na pasta temporária
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(temp_dir)
            logger.info(f"Arquivos extraídos com sucesso de {file.filename}")

        for nome_arquivo in os.listdir(temp_dir):

            # Ignorar o próprio arquivo ZIP salvo na pasta temporária
            if nome_arquivo == file.filename:
                continue

            caminho_arquivo = os.path.join(temp_dir, nome_arquivo)
            tamanho_arquivo = os.path.getsize(caminho_arquivo)

            if os.path.isfile(caminho_arquivo):
                extensao = Path(nome_arquivo).suffix.lower().strip(".")

                with open(caminho_arquivo, "rb") as f:
                    conteudo = f.read()

                if extensao in ["jpg", "jpeg", "png"]:
                    texto = ocr_image(conteudo, "por")
                    logger.info(f"OCR imagem executado: {nome_arquivo}")
                    arquivos_extraidos.append(nome_arquivo)

                elif extensao == "pdf":
                    resultado_pdf = ocr_pdf(conteudo, lang="por")
                    texto = ("\n\n\n\n\n").join([p["text"] for p in resultado_pdf])
                    logger.info(f"OCR PDF executado: {nome_arquivo}")
                    arquivos_extraidos.append(nome_arquivo)

                else:
                    logger.warning(f"Extensão não suportada no .zip: {nome_arquivo}")
                    texto = f"Tipo de arquivo '{extensao}' não suportado."
                    arquivos_rejeitados.append(nome_arquivo)

                resultados.append(
                    {
                        "file_name": nome_arquivo,
                        "file_size": float(tamanho_arquivo),
                        "text_output": texto,
                    }
                )

    except Exception as e:
        logger.error(f"Erro ao processar arquivo ZIP: {str(e)}")
        return JSONResponse(
            status_code=500, content={"error": "Erro ao processar o ZIP."}
        )

    return ZipExtractionResponse(
        total_files=len(arquivos_rejeitados) + len(arquivos_extraidos),
        processed_files=arquivos_extraidos,
        unsupported_files=arquivos_rejeitados,
        results=resultados,
    )


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

    return RecognitionPDFFileOutput(
        file_name=file.filename, file_size=file.size, text_output=full_text
    )
