# src/models/schemas.py
from pydantic import BaseModel
from typing import List, Optional

ALLOWED = {"image/jpeg", "image/png"}


class RecognitionImageFileOutput(BaseModel):
    file_name: str
    file_size: float
    text_output: str

class ZipExtractionResponse(BaseModel):
    """
    Schema para multiplos arquivos OCR compactados em formato ZIP
    """

    total_files: int
    processed_files: List[str]
    unsupported_files: Optional[List[str]] = None
    results: List[RecognitionImageFileOutput]

    class Config:
        json_schema_extra = {
            "example": {
                "total_files": 2,
                "processed_files": ["imagem1.png", "texto.pdf"],
                "unsupported_files": [],
                "results":
                [
                    {
                        "file_name": "imagem1.png",
                        "file_size": 40.5,
                        "text_output": "Bem vindo ao Tesseract!",
                    },
                    {
                        "file_name": "texto.pdf",
                        "file_size": 40.5,
                        "text_output": "Leitura de PDF!",
                    }
                ]
            }
        }