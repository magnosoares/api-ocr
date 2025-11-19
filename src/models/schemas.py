from fastapi import UploadFile
from pydantic import BaseModel, validator

# class ImageUploadForOCR(BaseModel):
#     file: UploadFile

#     @validator("file")
#     def validate_file_type(cls, v: UploadFile):
#         allowed_types = ["image/jpeg", "image/png"]
#         if v.content_type not in allowed_types:
#             raise ValueError("Formato inválido. Use JPEG ou PNG.")
#         return v

class RecognitionFileOutput(BaseModel):
    """
    Schema for OCR file output
    """
    file_name: str
    file_size: float
    text_output: str