# API Usage Guide

## Table of Contents

- [PDF Service](#pdf-service)
  - [PDF to Images](#pdf-to-images-endpoint)
- [YouTube Service](#youtube-service)
  - [Get Channel ID](#get-channel-id)
  - [Get Subscriptions](#get-subscriptions)

---

# PDF Service

## PDF to Images Endpoint

**Endpoint:** `POST /api/v1/pdf-to-images`

**Authentication:** Required via `x-api-key` header

**Query Parameters:**
- `output_format` (optional): Output format for images
  - `base64` (default) - Base64-encoded JPEG string
  - `binary` - Raw JPEG bytes as array
  - `both` - Both base64 and binary formats
- `dpi` (optional): Image resolution in DPI (dots per inch)
  - Range: 72-600
  - Default: 200
  - Higher values produce larger, more detailed images while maintaining aspect ratio
  - Lower values (e.g., 72-150) for smaller file sizes
  - Higher values (e.g., 300-600) for better quality

**Response Fields (per image):**
- `page` - Page number (1-indexed)
- `file_name` - Generated filename (e.g., "page_1.jpg")
- `width` - Image width in pixels
- `height` - Image height in pixels
- `mode` - Color mode (e.g., "RGB")
- `size_bytes` - Size of the JPEG file in bytes
- `base64` - Base64-encoded image data (if requested)
- `binary` - Raw JPEG bytes as array (if requested)

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
      "width": 1654,
      "height": 2339,
      "mode": "RGB",
      "size_bytes": 245678,
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
      "width": 1654,
      "height": 2339,
      "mode": "RGB",
      "size_bytes": 245678,
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
      "width": 1654,
      "height": 2339,
      "mode": "RGB",
      "size_bytes": 245678,
      "base64": "/9j/4AAQSkZJRgABAQEAYABgAAD...",
      "binary": [255, 216, 255, 224, 0, 16, 74, 70, ...]
    }
  ]
}
```

---

## Resolution Control

### Setting Custom DPI

Control the output image resolution using the `dpi` parameter. Higher DPI values create larger, more detailed images while maintaining the original aspect ratio.

**Low Resolution (72 DPI) - Smallest file size:**
```bash
curl -X POST "http://localhost:2277/api/v1/pdf-to-images?dpi=72" \
  -H "x-api-key: your-key" \
  -F "file=@document.pdf"
```

**Standard Resolution (200 DPI) - Default:**
```bash
curl -X POST "http://localhost:2277/api/v1/pdf-to-images?dpi=200" \
  -H "x-api-key: your-key" \
  -F "file=@document.pdf"
```

**High Resolution (300 DPI) - Print quality:**
```bash
curl -X POST "http://localhost:2277/api/v1/pdf-to-images?dpi=300" \
  -H "x-api-key: your-key" \
  -F "file=@document.pdf"
```

**Maximum Resolution (600 DPI) - Maximum detail:**
```bash
curl -X POST "http://localhost:2277/api/v1/pdf-to-images?dpi=600" \
  -H "x-api-key: your-key" \
  -F "file=@document.pdf"
```

### Combining Parameters

**High resolution with binary output:**
```bash
curl -X POST "http://localhost:2277/api/v1/pdf-to-images?dpi=300&output_format=binary" \
  -H "x-api-key: your-key" \
  -F "file=@document.pdf"
```

**Python example with custom DPI:**
```python
import requests

with open("document.pdf", "rb") as f:
    files = {"file": ("document.pdf", f, "application/pdf")}
    headers = {"x-api-key": "your-secret-key"}
    params = {"dpi": 300, "output_format": "base64"}
    
    response = requests.post(
        "http://localhost:2277/api/v1/pdf-to-images",
        files=files,
        headers=headers,
        params=params
    )
    
    data = response.json()
    print(f"Converted {data['pages']} pages at 300 DPI")
    print(f"First page size: {data['images'][0]['width']}x{data['images'][0]['height']}")
```

### DPI Recommendations

| Use Case | Recommended DPI | Notes |
|----------|----------------|-------|
| Web thumbnails | 72-100 | Smallest file size, fast processing |
| Web display | 150-200 | Good balance of quality and size |
| Document archival | 200-300 | Standard quality preservation |
| Print documents | 300 | Standard print quality |
| High-quality print | 600 | Maximum detail, large file sizes |

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
5. **Query Parameters** (optional):
   - Name: `output_format`, Value: `base64` (or `binary`, `both`)
   - Name: `dpi`, Value: `200` (or any value 72-600)
6. **Body:**
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

**400 Bad Request (Invalid DPI)**
```json
{
  "detail": "DPI must be between 72 and 600. Got: 1000"
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
- **Output:** JPEG images at configurable DPI (72-600, default 200)
- **Processing:** Synchronous (response waits for conversion)
- **Aspect Ratio:** Always maintained regardless of DPI setting

---

## Performance

Typical conversion times (at 200 DPI):
- 1-page PDF: ~1 second
- 5-page PDF: ~3-5 seconds
- 10-page PDF: ~8-10 seconds

**Note:** Higher DPI values will increase processing time and output file sizes proportionally.

For large PDFs or batch processing, consider:
- Using lower DPI (72-150) for faster processing
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

---

# YouTube Service

The YouTube service provides endpoints for extracting channel information.

**Base URL:** `/api/v1/youtube`

**Rate Limit:** 5 requests per minute (per IP)

---

## Get Channel ID

Extract the unique channel ID (UCID) from any YouTube channel URL.

**Endpoint:** `GET /api/v1/youtube/channel-id`

**Use Case:** Convert `@handle` URLs to stable channel IDs that never change.

### Request

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | Yes | YouTube channel URL |

**Supported URL formats:**
- `https://www.youtube.com/@handle`
- `https://www.youtube.com/channel/UCxxxxxxxx`
- `https://www.youtube.com/c/channelname`
- `https://www.youtube.com/user/username`

**Note:** URL-encoded URLs are automatically decoded (e.g., `https%3A%2F%2Fwww.youtube.com%2F%40handle` works correctly).

### cURL Example

```bash
curl -X GET "http://localhost:2277/api/v1/youtube/channel-id?url=https://www.youtube.com/@Fireship" \
  -H "x-api-key: your-secret-key"
```

### Response

```json
{
  "channel_id": "UCsBjURrPoezykLs9EqgamOA",
  "channel_url": "https://www.youtube.com/channel/UCsBjURrPoezykLs9EqgamOA"
}
```

### n8n Configuration

**HTTP Request Node:**

| Setting | Value |
|---------|-------|
| Method | `GET` |
| URL | `http://your-server:2277/api/v1/youtube/channel-id` |
| Authentication | None |
| Headers | `x-api-key`: `your-secret-key` |
| Query Parameters | `url`: `{{ $json.channel_url }}` |

**n8n Expression Example:**
```
{{ $json.channel_id }}
```

---

## Get Subscriptions

Get public subscriptions for a YouTube channel.

**Endpoint:** `GET /api/v1/youtube/subscriptions`

**Requirement:** Channel subscriptions must be set to **public** in YouTube settings.

### Request

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `channel_id` | string | No | env value | Channel ID (UC...) |
| `max_results` | integer | No | 50 | Results per page (1-50) |

### cURL Examples

**Using default channel (from .env):**
```bash
curl -X GET "http://localhost:2277/api/v1/youtube/subscriptions" \
  -H "x-api-key: your-secret-key"
```

**With specific channel:**
```bash
curl -X GET "http://localhost:2277/api/v1/youtube/subscriptions?channel_id=UC6S2pe9IBZkRuY1T_yZnIWQ&max_results=10" \
  -H "x-api-key: your-secret-key"
```

### Response

```json
{
  "total_results": 45,
  "subscriptions": [
    {
      "channel_name": "Fireship",
      "channel_id": "UCsBjURrPoezykLs9EqgamOA",
      "channel_url": "https://www.youtube.com/channel/UCsBjURrPoezykLs9EqgamOA",
      "description": "High-intensity code tutorials...",
      "thumbnail": "https://yt3.ggpht.com/..."
    },
    {
      "channel_name": "n8n",
      "channel_id": "UCiFwARNDOICtXFzpbsqqV6g",
      "channel_url": "https://www.youtube.com/channel/UCiFwARNDOICtXFzpbsqqV6g",
      "description": "Workflow automation...",
      "thumbnail": "https://yt3.ggpht.com/..."
    }
  ]
}
```

### n8n Configuration

**HTTP Request Node:**

| Setting | Value |
|---------|-------|
| Method | `GET` |
| URL | `http://your-server:2277/api/v1/youtube/subscriptions` |
| Authentication | None |
| Headers | `x-api-key`: `your-secret-key` |
| Query Parameters | `channel_id`: `UC...` (optional), `max_results`: `50` (optional) |

**n8n Expression to loop through subscriptions:**
```
{{ $json.subscriptions }}
```

**Get first subscription name:**
```
{{ $json.subscriptions[0].channel_name }}
```

---

## YouTube Error Responses

**400 Bad Request:**
```json
{
  "detail": "Channel URL is required"
}
```

**400 Forbidden (Private Subscriptions):**
```json
{
  "detail": "Error 403: Forbidden. The subscriptions are still marked as 'Private' in the YouTube account settings."
}
```

**404 Not Found:**
```json
{
  "detail": "Channel not found. Please check the URL."
}
```

**429 Too Many Requests:**
```json
{
  "detail": "Rate limit exceeded: 5 per 1 minute"
}
```

---

## Complete n8n Workflow Example

### Use Case: Get Channel IDs for Multiple Handles

```
[Manual Trigger] → [Set URLs] → [Split In Batches] → [HTTP Request] → [Merge Results]
```

**Step 1: Set URLs Node**
```json
{
  "urls": [
    "https://www.youtube.com/@Fireship",
    "https://www.youtube.com/@n8n-io",
    "https://www.youtube.com/@AllAboutAI"
  ]
}
```

**Step 2: HTTP Request Node (in loop)**
- URL: `http://your-server:2277/api/v1/youtube/channel-id`
- Query: `url` = `{{ $json.urls[$itemIndex] }}`
- Header: `x-api-key` = `your-secret-key`

**Step 3: Output**
Each iteration returns:
```json
{
  "channel_id": "UCsBjURrPoezykLs9EqgamOA",
  "channel_url": "https://www.youtube.com/channel/UCsBjURrPoezykLs9EqgamOA"
}
```

---

## Support

For issues or questions:
- GitHub: https://github.com/vcentea/n8n_utility_server
- See: [POPPLER_SETUP.md](POPPLER_SETUP.md) for Poppler issues
- See: [INSTALLATION.md](INSTALLATION.md) for setup help

