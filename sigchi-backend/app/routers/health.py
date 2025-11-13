from fastapi import APIRouter

router = APIRouter(tags=["Health"])

@router.get("/health")
def health_check():
    return {
        "status": "OK",
        "system": "SIGCHI",
        "message": "API running"
    }
