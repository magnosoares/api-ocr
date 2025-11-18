# api-ocr/src/api/routes/about.py

from fastapi import APIRouter


router = APIRouter(prefix="/about", tags = ["About"])

@router.get("/", status_code = 200)
def about():
    """
    Developers
    """
    return [
        {
            "name": "Tiago André da Silveira Fialho",
            "CPF": "953.049.671-00"
        },
        {
            "name": "Magno",
            "CPF": "123456"
        },
        {
            "name": "Lúcia Helena",
            "CPF": "987654321"
        },
        {
            "name": "Thiago Lobo",
            "CPF": "45678"
        }
    ]
