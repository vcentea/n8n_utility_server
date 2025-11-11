import os
import uuid
import base64
import shutil
from typing import Any, Dict, List

from pdf2image import convert_from_bytes
from pdf2image.exceptions import PDFInfoNotInstalledError, PDFPageCountError

from app.config import POPPLER_PATH, TEMP_PATH

DPI = 200
IMAGE_FORMAT = "JPEG"


def convert_to_images(pdf_bytes: bytes) -> List[Dict[str, Any]]:
    session_id = str(uuid.uuid4())
    temp_dir = os.path.join(TEMP_PATH, session_id)
    
    try:
        os.makedirs(temp_dir, exist_ok=True)

        convert_kwargs = {"dpi": DPI, "fmt": IMAGE_FORMAT.lower()}
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
        for idx, image in enumerate(images, start=1):
            file_name = f"page_{idx}.jpg"
            file_path = os.path.join(temp_dir, file_name)
            
            image.save(file_path, IMAGE_FORMAT)
            
            with open(file_path, "rb") as img_file:
                img_bytes = img_file.read()
                base64_str = base64.b64encode(img_bytes).decode("utf-8")
            
            result.append({
                "page": idx,
                "file_name": file_name,
                "base64": base64_str
            })
        
        return result
    
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

