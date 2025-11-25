# src/models/schemas.py
from pydantic import BaseModel
from typing import List
import magic

_mime = magic.Magic(mime=True)

ALLOWED = {"image/jpeg", "image/png"}


class RecognitionImageFileOutput(BaseModel):
    file_name: str
    file_size: float
    text_output: str

class OCRResult(BaseModel):
    arquivo: str
    ocorrencias: int
    trechos: List[str]
    texto_ocr: str

class SearchResponse(BaseModel):
    termo_buscado: str
    total_arquivos_processados: int
    resultados: List[OCRResult]
