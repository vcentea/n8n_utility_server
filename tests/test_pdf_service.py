import os
import base64
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def create_test_pdf(num_pages: int = 2) -> bytes:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    
    for i in range(1, num_pages + 1):
        pdf.drawString(100, 750, f"Test Page {i}")
        pdf.showPage()
    
    pdf.save()
    buffer.seek(0)
    return buffer.read()


def test_convert_pdf():
    from app.services.pdf_converter import convert_to_images
    
    pdf_bytes = create_test_pdf(2)
    
    result = convert_to_images(pdf_bytes)
    
    assert len(result) == 2
    assert result[0]["page"] == 1
    assert result[1]["page"] == 2
    assert "base64" in result[0]
    assert "file_name" in result[0]
    
    base64.b64decode(result[0]["base64"])
    
    print("✓ PDF conversion test passed")


if __name__ == "__main__":
    test_convert_pdf()

