from fastapi import APIRouter

from app.routes import pdf_service

api_router = APIRouter()

api_router.include_router(pdf_service.router, prefix="/v1", tags=["pdf"])

