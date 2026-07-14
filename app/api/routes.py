from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def root():
    return{
        "message": "masok coy anying"
    }

@router.get("/helth")
def helth():
    return{
        "status": "online cak",
        "backend": "FastAPI coy",
        "version": "1.0.0"
    }
