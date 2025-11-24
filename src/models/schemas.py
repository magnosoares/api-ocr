# src/api/models/schemas.py

import logging
import os
from fastapi import UploadFile, HTTPException
from pydantic import BaseModel, field_validator, validator

logger = logging.getLogger(__name__)


class RecognitionImageFileInput(BaseModel):
    file: UploadFile

    @field_validator("file")
    def validate_image_file(cls, file):
        running_tests = "PYTEST_CURRENT_TEST" in os.environ

        # tamanho
        try:
            if file.size is not None:
                size_bytes = file.size
            else:
                size_bytes = len(file.file.getvalue()) if running_tests else None
        except Exception:
            logger.error("Falha ao obter tamanho do arquivo enviado.")
            raise ValueError("Falha ao obter o tamanho do arquivo enviado.")

        # valida tipo
        if file.content_type not in ("image/jpeg", "image/png"):
            logger.error(
                f"Arquivo inválido enviado: {file.filename} | "
                f"Tipo: {file.content_type} | "
                f"Tamanho: {size_bytes} bytes"
            )
            raise ValueError("Formato de arquivo inválido. São aceitos apenas JPEG e PNG.")

        return file



class RecognitionImageFileOutput(BaseModel):
    """
    Schema for OCR file output
    """
    file_name: str
    file_size: float
    text_output: str