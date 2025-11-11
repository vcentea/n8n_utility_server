# API Usage Guide

## PDF to Images Endpoint

**Endpoint:** `POST /api/v1/pdf-to-images`

**Authentication:** Required via `x-api-key` header

**Query Parameters:**
- `output_format` (optional): Output format for images
  - `base64` (default) - Base64-encoded JPEG string
  - `binary` - Raw JPEG bytes as array
  - `both` - Both base64 and binary formats

---

## Output Format Examples

### Base64 (Default)
```bash
curl -X POST "http://localhost:2277/api/v1/pdf-to-images?output_format=base64" \
  -H "x-api-key: your-key" \
  -F "file=@document.pdf"
```

Response:
```json
{
  "pages": 1,
  "images": [
    {
      "page": 1,
      "file_name": "page_1.jpg",
      "base64": "/9j/4AAQSkZJRgABAQEAYABgAAD..."
    }
  ]
}
```

### Binary (Raw JPEG bytes)
```bash
curl -X POST "http://localhost:2277/api/v1/pdf-to-images?output_format=binary" \
  -H "x-api-key: your-key" \
  -F "file=@document.pdf"
```

Response:
```json
{
  "pages": 1,
  "images": [
    {
      "page": 1,
      "file_name": "page_1.jpg",
      "binary": [255, 216, 255, 224, 0, 16, 74, 70, ...]
    }
  ]
}
```

### Both Formats
```bash
curl -X POST "http://localhost:2277/api/v1/pdf-to-images?output_format=both" \
  -H "x-api-key: your-key" \
  -F "file=@document.pdf"
```

Response:
```json
{
  "pages": 1,
  "images": [
    {
      "page": 1,
      "file_name": "page_1.jpg",
      "base64": "/9j/4AAQSkZJRgABAQEAYABgAAD...",
      "binary": [255, 216, 255, 224, 0, 16, 74, 70, ...]
    }
  ]
}
```

---

## Binary Upload Methods

The endpoint accepts PDF files as binary data in multiple ways:

### Method 1: Multipart Form Upload (Recommended)

**Standard file upload - works with all HTTP clients**

```bash
curl -X POST http://localhost:2277/api/v1/pdf-to-images \
  -H "x-api-key: your-secret-key" \
  -F "file=@document.pdf"
```

**Python:**
```python
import requests

with open("document.pdf", "rb") as f:
    files = {"file": ("document.pdf", f, "application/pdf")}
    headers = {"x-api-key": "your-secret-key"}
    
    response = requests.post(
        "http://localhost:2277/api/v1/pdf-to-images",
        files=files,
        headers=headers
    )
    
    data = response.json()
    print(f"Converted {data['pages']} pages")
```

**JavaScript (Node.js):**
```javascript
const FormData = require('form-data');
const fs = require('fs');

const form = new FormData();
form.append('file', fs.createReadStream('document.pdf'));

fetch('http://localhost:2277/api/v1/pdf-to-images', {
  method: 'POST',
  headers: {
    'x-api-key': 'your-secret-key',
    ...form.getHeaders()
  },
  body: form
})
.then(res => res.json())
.then(data => console.log(`Converted ${data.pages} pages`));
```

---

### Method 2: Binary Stream Upload

**Upload PDF binary data directly from memory**

```python
import requests

# Get PDF binary data (e.g., from another API or database)
pdf_binary = get_pdf_from_somewhere()

files = {"file": ("document.pdf", pdf_binary, "application/pdf")}
headers = {"x-api-key": "your-secret-key"}

response = requests.post(
    "http://localhost:2277/api/v1/pdf-to-images",
    files=files,
    headers=headers
)
```

---

### Method 3: Pipe Binary Data (cURL)

**Stream PDF directly from stdin**

```bash
cat document.pdf | curl -X POST http://localhost:2277/api/v1/pdf-to-images \
  -H "x-api-key: your-secret-key" \
  -F "file=@-;type=application/pdf"
```

**From URL:**
```bash
wget -qO- https://example.com/document.pdf | \
  curl -X POST http://localhost:2277/api/v1/pdf-to-images \
  -H "x-api-key: your-secret-key" \
  -F "file=@-;type=application/pdf"
```

---

## n8n Integration

### HTTP Request Node Configuration

1. **Method:** `POST`
2. **URL:** `http://your-server:2277/api/v1/pdf-to-images`
3. **Authentication:** None (use Headers instead)
4. **Headers:**
   - Name: `x-api-key`
   - Value: `your-secret-key`
5. **Body:**
   - Content Type: `Form-Data Multipart`
   - Add Field:
     - Name: `file`
     - Type: `Binary Data`
     - Input Binary Field: Select your PDF binary data field

### n8n Example Workflow

```
[Trigger] → [Read Binary File] → [HTTP Request] → [Process Images]
```

**HTTP Request Node Settings:**
- **Send Binary Data:** Yes
- **Binary Property:** `data` (or your binary field name)
- **Parameter Name:** `file`
- **Content Type:** `application/pdf`

---

## Response Format

### Success (200 OK)

**Base64 format (default):**
```json
{
  "pages": 3,
  "images": [
    {
      "page": 1,
      "file_name": "page_1.jpg",
      "base64": "iVBORw0KGgoAAAANSUhEUgAA..."
    },
    {
      "page": 2,
      "file_name": "page_2.jpg",
      "base64": "iVBORw0KGgoAAAANSUhEUgAA..."
    }
  ]
}
```

**Binary format:**
```json
{
  "pages": 2,
  "images": [
    {
      "page": 1,
      "file_name": "page_1.jpg",
      "binary": [255, 216, 255, 224, 0, 16, 74, 70, ...]
    }
  ]
}
```

**Both formats:**
```json
{
  "pages": 1,
  "images": [
    {
      "page": 1,
      "file_name": "page_1.jpg",
      "base64": "iVBORw0KGgoAAAANSUhEUgAA...",
      "binary": [255, 216, 255, 224, 0, 16, 74, 70, ...]
    }
  ]
}
```

**Fields:**
- `pages`: Total number of pages converted
- `images`: Array of converted images
  - `page`: Page number (1-indexed)
  - `file_name`: Generated filename
  - `base64`: Base64-encoded JPEG image data (if output_format is 'base64' or 'both')
  - `binary`: Raw JPEG bytes as array (if output_format is 'binary' or 'both')

---

### Error Responses

**400 Bad Request**
```json
{
  "detail": "Invalid or missing PDF file"
}
```

**401 Unauthorized**
```json
{
  "detail": "Unauthorized"
}
```

**413 Payload Too Large**
```json
{
  "detail": "File too large. Maximum size is 10485760 bytes"
}
```

**500 Internal Server Error**
```json
{
  "detail": "Error converting PDF: [error message]"
}
```

---

## Working with Images

### Base64 Format

**Decode and Save (Python):**
```python
import base64
from pathlib import Path

response = requests.post(
    "http://localhost:2277/api/v1/pdf-to-images",
    files={"file": open("doc.pdf", "rb")},
    headers={"x-api-key": "your-key"},
    params={"output_format": "base64"}
).json()

for img in response['images']:
    img_data = base64.b64decode(img['base64'])
    Path(f"output_{img['file_name']}").write_bytes(img_data)
```

**Decode and Save (Node.js):**
```javascript
const fs = require('fs');

response.images.forEach(img => {
  const buffer = Buffer.from(img.base64, 'base64');
  fs.writeFileSync(`output_${img.file_name}`, buffer);
});
```

**Display in HTML:**
```html
<img src="data:image/jpeg;base64,{base64_string_here}" alt="Page 1">
```

### Binary Format

**Save Directly (Python):**
```python
response = requests.post(
    "http://localhost:2277/api/v1/pdf-to-images",
    files={"file": open("doc.pdf", "rb")},
    headers={"x-api-key": "your-key"},
    params={"output_format": "binary"}
).json()

for img in response['images']:
    # Convert array to bytes
    img_bytes = bytes(img['binary'])
    Path(f"output_{img['file_name']}").write_bytes(img_bytes)
```

**Save Directly (Node.js):**
```javascript
response.images.forEach(img => {
  const buffer = Buffer.from(img.binary);
  fs.writeFileSync(`output_${img.file_name}`, buffer);
});
```

### Which Format to Use?

| Format | Use Case | Pros | Cons |
|--------|----------|------|------|
| **base64** | Web apps, JSON APIs, embed in HTML | Easy to handle, text-based | ~33% larger |
| **binary** | File storage, processing pipelines | Smaller size, native format | Requires conversion |
| **both** | Flexibility, immediate use + storage | Best of both | Largest response |

---

## Testing

### Quick Test

```bash
# Using test script
python test_binary_upload.py document.pdf

# Using curl
curl -X POST http://localhost:2277/api/v1/pdf-to-images \
  -H "x-api-key: supersecretapikey" \
  -F "file=@document.pdf" | jq
```

### Test Script

Run comprehensive tests:

```bash
python test_binary_upload.py path/to/your.pdf
```

This tests:
- ✓ Multipart form upload
- ✓ Binary stream upload
- ✓ In-memory binary data
- ✓ Shows curl examples

---

## Limitations

- **Max File Size:** 10 MB (configurable in `app/config.py`)
- **Format:** PDF only
- **Output:** JPEG images at 200 DPI
- **Processing:** Synchronous (response waits for conversion)

---

## Performance

Typical conversion times:
- 1-page PDF: ~1 second
- 5-page PDF: ~3-5 seconds
- 10-page PDF: ~8-10 seconds

For large PDFs or batch processing, consider:
- Increasing timeout settings in your HTTP client
- Processing files asynchronously
- Splitting large PDFs into smaller chunks

---

## Security

- ✅ API key authentication required
- ✅ File type validation
- ✅ Size limit enforcement
- ✅ Temporary files cleaned up immediately
- ✅ No permanent storage

**Important:** Keep your API key secure. Don't commit it to version control.

---

## Common Issues

### "Unauthorized" Error
- Check that `x-api-key` header is set correctly
- Verify the API key matches your `.env` file

### "Invalid or missing PDF file"
- Ensure content type is `application/pdf`
- Verify the file is a valid PDF

### "File too large"
- Maximum size is 10 MB by default
- Compress your PDF or split into smaller files

### Timeout Errors
- Large PDFs take longer to process
- Increase your HTTP client timeout
- Default server has no timeout limit

---

## API Documentation

Interactive API documentation available at:
- **Swagger UI:** http://localhost:2277/docs
- **ReDoc:** http://localhost:2277/redoc

---

## Support

For issues or questions:
- GitHub: https://github.com/vcentea/n8n_utility_server
- See: [POPPLER_SETUP.md](POPPLER_SETUP.md) for Poppler issues
- See: [INSTALLATION.md](INSTALLATION.md) for setup help

