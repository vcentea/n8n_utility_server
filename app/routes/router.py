from fastapi import APIRouter

from app.services.pdf.routes import router as pdf_router
from app.services.youtube.routes import router as youtube_router
from app.services.youtube.rss_routes import router as youtube_rss_router
from app.services.youtube.transcript_routes import router as youtube_transcript_router

api_router = APIRouter()

api_router.include_router(pdf_router, prefix="/v1/pdf", tags=["pdf"])
api_router.include_router(pdf_router, prefix="/v1", tags=["pdf"])
api_router.include_router(youtube_router, prefix="/v1/youtube", tags=["youtube"])
api_router.include_router(youtube_rss_router, prefix="/v1/youtube", tags=["youtube-rss"])
api_router.include_router(youtube_transcript_router, prefix="/v1/youtube", tags=["youtube-transcript"])

