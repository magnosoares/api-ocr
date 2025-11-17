from fastapi import FastAPI, HTTPException, File, UploadFile
from src.models.schemas import ImageUploadForOCR
import logging
import pytesseract
from PIL import Image
import io
import re

# Caminho do executável
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="API - Automação OCR")

@app.get("/")
def api_ocr():
    """Endpoint de health check"""
    return {"status": "ok", "message": "API funcionando"}

@app.post("/ocr/texto")
def text_from_file(file: UploadFile = File(...)):
    # validação simples
    if file.content_type not in ["image/jpeg", "image/png"]:
        return {"error": "Formato inválido. Use JPEG ou PNG."}

    # leitura da imagem
    image_bytes = file.file.read()
    image = Image.open(io.BytesIO(image_bytes))
    
    # processamento OCR
    texto = pytesseract.image_to_string(image, lang="por")
    texto = re.sub(r"\s+", " ", texto.replace("\n", " ").replace("\r", " ").replace("\t", " "))
    
    return {"text": texto}
