# tests/test_recognition_image_file.py
#from fastapi import Path
from fastapi.testclient import TestClient
from pathlib import Path
from src.api.main import app
from src.models.schemas import RecognitionImageFileOutput

client = TestClient(app)
FILES_DIR = Path(__file__).parent / "files"


# ---------------------------------------------------------------------
# Tests for input files
# ---------------------------------------------------------------------
def test_valid_image_jpeg():
    """
    Test for a valid jpeg image file
    """
    file_path = FILES_DIR / "image_test_ocr.jpeg"

    with open(file_path, "rb") as f:
        files = {"file": ("image_test_ocr.jpeg", f, "image/jpeg")}
        response = client.post("/recognition/image-file", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["file_name"] == "image_test_ocr.jpeg"

    text_from_file = data["text_output"].replace("\n", " ").strip()
    text_for_test = "Cedric himself knew nothing whatever about it. It had never been even mentioned to him. He knew that his papa had been an Englishman, becanse his mamma had told him so; but then his papa had died when he was so litle a boy that he could not remember very much about him. except that he was big, and had blue eyes and a long mustache, and that it was a splendid thing to be carried around the room on his shoulder."
    
    assert text_from_file == text_for_test
    


def test_valid_image_png():
    """
    Test for a valid png image file
    """
    file_path = FILES_DIR / "image_test_ocr.png"

    with open(file_path, "rb") as f:
        files = {"file": ("image_test_ocr.png", f, "image/png")}
        response = client.post("/recognition/image-file", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["file_name"] == "image_test_ocr.png"
    
    text_from_file = data["text_output"].replace("\n", " ").strip()
    text_for_test = "Noisy Image to test Tesseract OCR"
    assert text_from_file == text_for_test


def test_invalid_file_pdf():
    """
    Test for a invalid type file, Such as a pdf file.
    """
    file_path = FILES_DIR / "image_test_ocr.pdf"
    
    with open(file_path, "rb") as f:
        files = {"file": ("image_test_ocr.pdf", f, "application/pdf")} 
        response = client.post("/recognition/image-file", files=files)

    assert response.status_code == 400 
    data = response.json()
    
    detail = data.get("detail", "")
    assert "Tipo de arquivo inválido. Somente" in detail 

    assert "image/jpeg" in detail
    assert "image/png" in detail
    
    assert "são permitidos." in detail

# ---------------------------------------------------------------------
# Tests for output schemas
# ---------------------------------------------------------------------

def test_output_schema_jpeg():
    # carrega arquivo real
    file_path = FILES_DIR / "image_test_ocr.jpeg"
    real_size_kb = round(file_path.stat().st_size / 1000, 1)

    # simula saída do OCR
    output = RecognitionImageFileOutput(
        file_name="image_test_ocr.jpeg",
        file_size=real_size_kb,
        text_output="Cedric himself knew nothing whatever about it. It had never been even mentioned to him. He knew that his papa had been an Englishman, becanse his mamma had told him so; but then his papa had died when he was so litle a boy that he could not remember very much about him. except that he was big, and had blue eyes and a long mustache, and that it was a splendid thing to be carried around the room on his shoulder."
    )

    assert output.file_name == "image_test_ocr.jpeg"
    assert output.file_size == real_size_kb
    assert output.text_output == "Cedric himself knew nothing whatever about it. It had never been even mentioned to him. He knew that his papa had been an Englishman, becanse his mamma had told him so; but then his papa had died when he was so litle a boy that he could not remember very much about him. except that he was big, and had blue eyes and a long mustache, and that it was a splendid thing to be carried around the room on his shoulder."

def test_output_schema_png():
    # carrega arquivo real
    file_path = FILES_DIR / "image_test_ocr.png"
    real_size_kb = round(file_path.stat().st_size / 1000, 1)

    # simula saída do OCR
    output = RecognitionImageFileOutput(
        file_name="image_test_ocr.png",
        file_size=real_size_kb,
        text_output="Noisy Image to test Tesseract OCR"
    )

    assert output.file_name == "image_test_ocr.png"
    assert output.file_size == real_size_kb
    assert output.text_output == "Noisy Image to test Tesseract OCR"
