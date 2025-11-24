# src/api/models/schemas.py

import logging
from fastapi import UploadFile, HTTPException
from pydantic import BaseModel, field_validator, validator

logger = logging.getLogger(__name__)

# class ImageUploadForOCR(BaseModel):
#     file: UploadFile

#     @validator("file")
#     def validate_file_type(cls, v: UploadFile):
#         allowed_types = ["image/jpeg", "image/png"]
#         if v.content_type not in allowed_types:
#             raise ValueError("Formato inválido. Use JPEG ou PNG.")
#         return v

# class RecognitionFileInput(BaseModel):
#     content_type: str
#     size: int


#     @field_validator("content_type")
#     def validate_file_type(cls, v):
#         allowed_types = ["image/jpeg", "image/png"]
#         if v not in allowed_types:
#             raise ValueError("Invalid file type. Use JPEG or PNG.")
#         return v
    
#     @field_validator("size")
#     def validate_size(cls, v):
#         if v > 10_485_760:
#             raise ValueError("File too large. Max 10 MB.")
#         return v
class RecognitionImageFileInput(BaseModel):
    file: UploadFile

    @field_validator("file")
    def validate_image_file(cls, file):

        logger.info(
            f"FILE INFO - Name: {file.filename}, ",
            f"Size: {(file.size / 1000):.1f}KB ",
            f"Content Type {file.content_type}"
        )

        allowed = ["image/jpeg", "image/png"]
        if file.content_type not in allowed:
            logger.error(f"Formato inválido: {file.content_type}")
            raise HTTPException(
                status_code=400,
                detail=f"Formato inválido. Permitidos: {allowed}"
            )
        
        return file


class RecognitionImageFileOutput(BaseModel):
    """
    Schema for OCR file output
    """
    file_name: str
    file_size: float
    text_output: str