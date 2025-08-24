from fastapi import APIRouter, status

router = APIRouter()

router.get("/health", status_code=status.HTTP_200_OK, summary="Health check")
async def health_check():
    return {"status": "healthy"}
