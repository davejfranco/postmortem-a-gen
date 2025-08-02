from fastapi import APIRouter, HTTPException, Depends, status

router = APIRouter()

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "ok"}


@router.post("/slack", status_code=status.HTTP_200_OK)
async def slack_event():
    return {"status": "ok"}
