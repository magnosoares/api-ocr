# api-ocr/src/api/routes/search.py

from typing import Literal
from fastapi import APIRouter, File, Form, HTTPException, Query, UploadFile
import logging
import io
import zipfile
import magic
from src.services.ocr_service import pesquisar_texto, ocr_image, ocr_pdf_texto
from src.models.schemas import SearchResponse


logger = logging.getLogger(__name__)
# Tipos permitidos (validação por conteúdo real)
TIPOS_PERMITIDOS = {"image/jpeg", "image/png", "application/pdf"}
mime_detector = magic.Magic(mime=True)

router = APIRouter(prefix="/search", tags = ["Search"])

@router.post("/img-file")
def search_text_in_img_file(file: UploadFile = File(...), 
                            lang: Literal["por", "eng", "fra", "spa"] = Query("por", description="Idioma do OCR"),
                            termo: str = Form(..., min_length=2, description="Texto para buscar (ex: CPF, nome, contrato)")):
    # validação simples
    if file.content_type not in ["image/jpeg", "image/png"]:
        return {"error": "Formato inválido. Use JPEG ou PNG."}
    image_bytes = file.file.read()
    # processamento OCR
    texto = ocr_image(image_bytes, lang)
    resultados = []
    
    resultados.append(pesquisar_texto(texto, termo, file.filename))

    return SearchResponse(
        termo_buscado=termo,
        total_arquivos_processados=1,
        resultados=resultados)
   


@router.post("/zip-files")
async def search_text_in_zip_files(zip_file: UploadFile = File(..., description="Arquivo ZIP com imagens e PDFs"), 
                                   lang: Literal["por", "eng", "fra", "spa"] = Query("por", description="Idioma do OCR"),
                                   termo: str = Form(..., min_length=2, description="Texto para buscar (ex: CPF, nome, contrato)")):
    
    """Validação completa e segura do arquivo ZIP"""
    if not zip_file.filename.lower().endswith('.zip'):
        raise HTTPException(400, detail="Apenas arquivos .zip são aceitos")

    contents = zip_file.file.read()
    if len(contents) == 0:
        raise HTTPException(400, detail="Arquivo vazio")

    if len(contents) > 100 * 1024 * 1024:  # 100 MB
        raise HTTPException(400, detail="Arquivo muito grande (máximo 100 MB)")

    # Validação por magic bytes
    tipo_real = mime_detector.from_buffer(contents[:2048])
    
    if tipo_real != "application/zip":
        raise HTTPException(400, detail=f"Arquivo não é um ZIP válido. Tipo detectado: {tipo_real}")

    # Testa se abre como ZIP
    try:
        with zipfile.ZipFile(io.BytesIO(contents)) as z:
            bad_file = z.testzip()
            if bad_file:
                raise HTTPException(400, detail=f"ZIP corrompido (arquivo com problema: {bad_file})")
    except zipfile.BadZipFile:
        raise HTTPException(400, detail="Arquivo ZIP inválido ou corrompido")

    logger.info(f"FILE INFO - Arquivo ZIP: {zip_file.filename}, Size: {(zip_file.size / 1000):.1f}KB")

    resultados = []
    arquivos_processados = 0

    with zipfile.ZipFile(io.BytesIO(contents)) as zip_file:
        for item in zip_file.infolist():
            if item.is_dir() or item.filename.startswith(('__MACOSX/', '.')):
                continue

            nome_arquivo = item.filename.split('/')[-1]  # pega só o nome

            arquivos_processados += 1
            logger.info(f"FILE INFO - Arquivo #{arquivos_processados}: {nome_arquivo}")

            try:
                with zip_file.open(item) as f:
                    dados = f.read()
            except Exception:
                continue  # arquivo criptografado ou corrompido

            # Validação por conteúdo real
            tipo = mime_detector.from_buffer(dados[:2048])

            if tipo not in TIPOS_PERMITIDOS:
                continue

            texto = ""

            try:
                if tipo.startswith("image/"):
                    texto += ocr_image(dados, lang)
                elif tipo == "application/pdf":
                    texto += ocr_pdf_texto(dados, lang)

            except Exception as e:
                logger.error(f"Falha ao ocerizar conteúdo do arquivo!")
                continue  # falha no OCR desse arquivo

            resultados.append(pesquisar_texto(texto, termo, nome_arquivo))


    return SearchResponse(
        termo_buscado=termo,
        total_arquivos_processados=arquivos_processados,
        resultados=resultados)