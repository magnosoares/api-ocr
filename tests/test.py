import pathlib
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_recognition_pdf_file_invalid_type():
    txt_path = pathlib.Path(__file__).parent / "files" / "Sample_01_jpeg.jpeg"
    txt_path.write_text("conteúdo não-PDF")

    with txt_path.open("rb") as f:
        response = client.post(
            "/recognition/pdf-file",
            files={"file": ("Sample_01_jpeg.jpeg", f, "image/jpeg")},
            params={"lang": "por"},
        )

    assert response.status_code == 400
    assert "Formato inválido" in response.json()["error"]


def test_recognition_pdf_file_success():
    # caminho para o PDF dentro de tests/files
    pdf_path = pathlib.Path(__file__).parent / "files" / "Sample_01_pdf.pdf"

    with pdf_path.open("rb") as f:
        response = client.post(
            "/recognition/pdf-file",
            files={"file": ("Sample_01_pdf.pdf", f, "application/pdf")},
            params={"lang": "por"},
        )

    assert response.status_code == 200

    data = response.json()

    # Verifica metadados
    assert data["file_name"] == "Sample_01_pdf.pdf"
    assert data["file_size"] > 0

    # Verifica que o texto não está vazio
    text = data["text_output"]
    assert isinstance(text, str)
    assert len(text.strip()) > 0

    # Checa palavras-chave esperadas no OCR
    assert "BALEIA AZUL" in text
    assert "TERMO DE COMPROMISSO E RESPONSABILIDADE DO SERVIDOR" in text
    assert "José da Silva, matrícula 0.000.000-0" in text
