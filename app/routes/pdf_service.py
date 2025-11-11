from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.pdf_converter import convert_to_images
from app.config import MAX_FILE_SIZE

router = APIRouter()


@router.post("/pdf-to-images")
async def pdf_to_images(file: UploadFile = File(...)):
    if not file.content_type or "pdf" not in file.content_type.lower():
        raise HTTPException(
            status_code=400,
            detail="Invalid or missing PDF file"
        )
    
    pdf_bytes = await file.read()
    
    if len(pdf_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE} bytes"
        )
    
    if len(pdf_bytes) == 0:
        raise HTTPException(
            status_code=400,
            detail="Empty file provided"
        )
    
    try:
        images = convert_to_images(pdf_bytes)
        
        return {
            "pages": len(images),
            "images": images
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error converting PDF: {str(e)}"
        )

