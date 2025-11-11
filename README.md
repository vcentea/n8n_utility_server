# Utility Service Platform

A minimal, production-deployable REST microservice for PDF-to-image conversion.

## Features

- **PDF to Images**: Convert PDF files to base64-encoded JPEG images
- **API Key Authentication**: Secure endpoints with static API key
- **Docker Support**: Fully containerized deployment
- **Structured Logging**: JSON-formatted logs for monitoring
- **FastAPI**: Modern, fast Python web framework

## Project Structure

```
utility-service/
├── app/
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration management
│   ├── core/
│   │   ├── auth.py          # API key middleware
│   │   ├── logger.py        # Logging setup
│   │   └── errors.py        # Error handling
│   ├── routes/
│   │   ├── router.py        # Router registration
│   │   └── pdf_service.py   # PDF conversion endpoint
│   └── services/
│       └── pdf_converter.py # PDF conversion logic
├── tests/
│   └── test_pdf_service.py
├── .env.example
├── Dockerfile
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.12+
- poppler-utils (for PDF processing)
- Docker (for containerized deployment)

## Installation

### Local Development

1. Clone the repository
2. Copy `.env.example` to `.env` and configure:

```bash
PORT=2277
API_KEY=your-secret-api-key
LOG_LEVEL=info
TEMP_PATH=/tmp/pdf_service
POPPLER_PATH=/path/to/poppler/bin  # required on Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Install poppler-utils:
   - **Ubuntu/Debian**: `sudo apt-get install poppler-utils`
   - **macOS**: `brew install poppler`
   - **Windows**: Download from https://blog.alivate.com.au/poppler-windows/

5. Run the application:

```bash
# Windows
start_local.bat

# Linux / macOS
chmod +x start_local.sh
./start_local.sh
```

### Docker Deployment

1. Build the image:

```bash
docker build -t utility-service .
```

2. Run the container:

```bash
docker run -d -p 2277:2277 --env-file .env utility-service
```

Or use environment variables directly:

```bash
docker run -d -p 2277:2277 \
  -e API_KEY=your-secret-api-key \
  -e PORT=2277 \
  utility-service
```

## API Documentation

### Authentication

All `/api/*` endpoints require an API key in the header:

```
x-api-key: your-secret-api-key
```

### Endpoints

#### Health Check

```
GET /health
```

Response:
```json
{
  "status": "healthy"
}
```

#### Convert PDF to Images

```
POST /api/v1/pdf-to-images
```

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: `file` (PDF file, max 10 MB)
- Header: `x-api-key: your-secret-api-key`

**Success Response (200):**
```json
{
  "pages": 3,
  "images": [
    {
      "page": 1,
      "file_name": "page_1.jpg",
      "base64": "base64-encoded-image-data..."
    },
    {
      "page": 2,
      "file_name": "page_2.jpg",
      "base64": "base64-encoded-image-data..."
    }
  ]
}
```

**Error Responses:**
- `400 Bad Request`: Invalid or missing PDF file
- `401 Unauthorized`: Missing or invalid API key
- `413 Payload Too Large`: File exceeds 10 MB
- `500 Internal Server Error`: Conversion error

### Testing with cURL

```bash
curl -X POST http://localhost:2277/api/v1/pdf-to-images \
  -H "x-api-key: your-secret-api-key" \
  -F "file=@sample.pdf"
```

### Testing with n8n

1. Add an **HTTP Request** node
2. Configure:
   - Method: `POST`
   - URL: `http://your-server:2277/api/v1/pdf-to-images`
   - Authentication: None (use headers)
   - Headers: `x-api-key: your-secret-api-key`
   - Body: Binary File Upload
   - Binary Property: Select your PDF input

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `2277` | Server port |
| `API_KEY` | Required | API authentication key |
| `LOG_LEVEL` | `info` | Logging level (debug, info, warning, error) |
| `TEMP_PATH` | `/tmp/pdf_service` | Temporary file storage path |
| `POPPLER_PATH` | _empty_ | Directory containing Poppler binaries (required on Windows) |

## Logging

Logs are output to stdout in JSON format:

```json
{
  "time": "2025-11-10T21:14:32Z",
  "level": "info",
  "method": "POST",
  "path": "/api/v1/pdf-to-images",
  "status": 200,
  "duration_ms": 4230
}
```

## Testing

Run the basic test:

```bash
python tests/test_pdf_service.py
```

Note: Requires `reportlab` package for test PDF generation:

```bash
pip install reportlab
```

## Performance

- Converts 5-page PDF in ~5 seconds
- DPI: 200 (configurable in `pdf_converter.py`)
- Output format: JPEG
- Temporary files cleaned up after conversion

## Security

- Static API key authentication
- No permanent file storage
- Maximum upload size enforced (10 MB)
- CORS disabled by default
- All temporary files cleaned up after processing

## Future Extensions

The architecture supports easy addition of new services:

- Voice transcription (Whisper)
- YouTube video processing
- OCR capabilities
- Async job queue

Each new service follows the same pattern:
1. Create `routes/<service>.py`
2. Create `services/<logic>.py`
3. Register in `routes/router.py`

## Deployment Requirements

**Minimum VM Specs:**
- 1 vCPU
- 1 GB RAM
- 10 GB storage

**Recommended:**
- 2 vCPU
- 2 GB RAM
- 20 GB storage

## License

MIT

## Support

For issues or questions, please open an issue in the repository.

