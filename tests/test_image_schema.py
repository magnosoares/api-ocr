# tests/test_image_schema.py
import pytest
from pydantic import ValidationError
from starlette.datastructures import Headers
from starlette.datastructures import UploadFile
from io import BytesIO
from src.models.schemas import RecognitionImageFileInput, RecognitionImageFileOutput

class FakeUploadFile:
    """
    Fake file (in memory only) for test
    """
    def __init__(self, filename: str, content_type: str, content: bytes = b"data"):
        self.filename = filename
        self.content_type = content_type
        self.file = BytesIO(content)
        self.size = len(content)

    def sync_read(self):
        self.file.seek(0)
        return self.file.read()

    async def read(self):
        return self.sync_read()

    def seek(self, offset: int, whence: int = 0):
        return self.file.seek(offset, whence)

def fake_upload_file(filename: str, content_type: str, content: bytes = b"data"):
    #Fake headers (Upload file get data from there)
    headers = Headers({"content-type": content_type})

    return UploadFile(
        filename=filename,
        file=BytesIO(content),
        headers=headers
    )


def test_valid_image_jpeg():
    file = fake_upload_file("foto.jpg", "image/jpeg")
    model = RecognitionImageFileInput(file=file)
    assert model.file.filename == "foto.jpg"
    assert model.file.content_type == "image/jpeg"


def test_valid_image_png():
    file = fake_upload_file("foto.png", "image/png")
    model = RecognitionImageFileInput(file=file)
    assert model.file.filename == "foto.png"
    assert model.file.content_type == "image/png"


def test_invalid_file_type():
    file = fake_upload_file("document.pdf", "application/pdf")
    with pytest.raises(ValidationError):
        RecognitionImageFileInput(file=file)


def test_output_schema():
    output = RecognitionImageFileOutput(
        file_name="foto.jpg",
        file_size=123.4,
        text_output="resultado OCR"
    )
    assert output.file_name == "foto.jpg"
    assert output.file_size == 123.4
    assert output.text_output == "resultado OCR"
