# src/models/schemas.py
from pydantic import BaseModel

ALLOWED = {"image/jpeg", "image/png"}


class RecognitionImageFileOutput(BaseModel):
    file_name: str
    file_size: float
    text_output: str
