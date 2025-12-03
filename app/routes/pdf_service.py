from enum import Enum
from fastapi import APIRouter, UploadFile, File, HTTPException, Query

from app.services.pdf_converter import convert_to_images
from app.config import MAX_FILE_SIZE

router = APIRouter()


class OutputFormat(str, Enum):
    BASE64 = "base64"
    BINARY = "binary"
    BOTH = "both"


@router.post("/pdf-to-images")
async def pdf_to_images(
    file: UploadFile = File(...),
    output_format: OutputFormat = Query(
        default=OutputFormat.BASE64,
        description="Output format: 'base64' (default), 'binary', or 'both'"
    ),
    dpi: int = Query(
        default=200,
        ge=72,
        le=600,
        description="Image resolution in DPI (72-600). Higher values produce larger, more detailed images while maintaining aspect ratio."
    )
):
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
        images = convert_to_images(
            pdf_bytes, 
            output_format=output_format.value,
            dpi=dpi
        )
        
        return {
            "pages": len(images),
            "images": images
        }
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error converting PDF: {str(e)}"
        )

