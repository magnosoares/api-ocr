import pathlib
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_ocr_zip_invalid_type():
    txt_path = pathlib.Path(__file__).parent / "files" / "Sample_01_jpeg.jpeg"

    with txt_path.open("rb") as f:
        response = client.post(
            "/recognition/zip-files",
            files={"file": ("Sample_01_jpeg.jpeg", f, "image/jpeg")},
            params={"lang": "por"},
        )

    assert response.status_code == 400
    assert "Formato inválido" in response.json()["error"]


def test_ocr_zip():

    # caminho do arquivo ZIP no projeto
    txt_path = pathlib.Path(__file__).parent / "files" / "TesteAPI.zip"

    # faz o upload simulando o envio real
    with txt_path.open("rb") as f:
        response = client.post(
            "/recognition/zip-files",
            files={"file": ("TesteAPI.zip", f, "application/x-zip-compressed")},
        )

    assert response.status_code == 200
    data = response.json()

    # verifica se os dois arquivos compactados foram extraídos
    assert "results" in data
    assert data["total_files"] == 2
