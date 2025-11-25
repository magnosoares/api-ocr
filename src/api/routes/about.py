# api-ocr/src/api/routes/about.py

from fastapi import APIRouter


router = APIRouter(prefix="/about", tags=["About"])


@router.get("/", status_code=200)
def about():
    """
    Equipe de Desenvolvedores
    """
    return [
        {"Nome": "Tiago André da Silveira Fialho", "Matrícula": "192.028-6"},
        {"Nome": "Magno Santana Soares", "Matrícula": "1.721.980-9"},
        {"Nome": "Lúcia Helena Dutra Magalhães", "Matrícula": "76.847-2"},
        {"Nome": "Thiago Lobo Leite", "Matrícula": "236.128-0"},
    ]
