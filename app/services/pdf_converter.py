import os
import uuid
import base64
import shutil
from typing import Any, Dict, List

from pdf2image import convert_from_bytes
from pdf2image.exceptions import PDFInfoNotInstalledError, PDFPageCountError

from app.config import POPPLER_PATH, TEMP_PATH

DEFAULT_DPI = 200
MIN_DPI = 72
MAX_DPI = 600
IMAGE_FORMAT = "JPEG"


def convert_to_images(
    pdf_bytes: bytes, 
    output_format: str = "base64",
    dpi: int = DEFAULT_DPI
) -> List[Dict[str, Any]]:
    """
    Convert PDF bytes to images in the specified format.
    
    Args:
        pdf_bytes: PDF file as bytes
        output_format: 'base64', 'binary', or 'both'
        dpi: Resolution in DPI (72-600, default: 200). Higher values produce 
             larger, more detailed images while maintaining aspect ratio.
    
    Returns:
        List of dictionaries containing page information and image data
    """
    if not MIN_DPI <= dpi <= MAX_DPI:
        raise ValueError(
            f"DPI must be between {MIN_DPI} and {MAX_DPI}. Got: {dpi}"
        )
    
    session_id = str(uuid.uuid4())
    temp_dir = os.path.join(TEMP_PATH, session_id)
    
    try:
        os.makedirs(temp_dir, exist_ok=True)

        convert_kwargs = {"dpi": dpi, "fmt": IMAGE_FORMAT.lower()}
        if POPPLER_PATH:
            convert_kwargs["poppler_path"] = POPPLER_PATH

        try:
            images = convert_from_bytes(pdf_bytes, **convert_kwargs)
        except PDFInfoNotInstalledError as exc:
            raise RuntimeError(
                "Poppler is not installed or POPPLER_PATH is incorrect."
            ) from exc
        except PDFPageCountError as exc:
            raise RuntimeError(
                "Unable to determine PDF page count. Verify the file is a valid PDF."
            ) from exc
        
        result = []
        total_images = len(images)
        
        for idx, image in enumerate(images, start=1):
            file_name = f"page_{idx}.jpg"
            file_path = os.path.join(temp_dir, file_name)
            
            # Get image info for debugging
            image_size = image.size
            image_mode = image.mode
            
            image.save(file_path, IMAGE_FORMAT)
            
            with open(file_path, "rb") as img_file:
                img_bytes = img_file.read()
            
            page_data = {
                "page": idx,
                "file_name": file_name,
                "width": image_size[0],
                "height": image_size[1],
                "mode": image_mode,
                "size_bytes": len(img_bytes)
            }
            
            if output_format in ("base64", "both"):
                page_data["base64"] = base64.b64encode(img_bytes).decode("utf-8")
            
            if output_format in ("binary", "both"):
                page_data["binary"] = list(img_bytes)
            
            result.append(page_data)
        
        return result
    
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

