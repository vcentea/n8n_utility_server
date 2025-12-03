# Utility Service Platform

A minimal, production-deployable REST microservice for PDF-to-image conversion.

## Features

- **PDF to Images**: Convert PDF files to JPEG images (base64, binary, or both)
- **Configurable Resolution**: Control output quality with DPI parameter (72-600)
- **API Key Authentication**: Secure endpoints with static API key
- **Docker Support**: Fully containerized deployment with easy updates
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

### 🐳 Docker (Recommended - Zero Configuration)

**Everything works out of the box!** Poppler is automatically included.

**First-time setup:**
```bash
cp .env.example .env              # Configure (edit API_KEY)
docker-compose up -d              # Start service
curl http://localhost:2277/health # Verify it's running
```

**Updating to latest version:**
```bash
# Linux / macOS
./update_docker.sh

# Windows
update_docker.bat
```

✅ **No Poppler installation needed**  
✅ **No manual dependencies**  
✅ **Works the same on all platforms**  
✅ **Easy updates with automatic git pull**

### 💻 Local Development

Requires manual setup of Poppler and Python dependencies.

**Quick Setup:**

```bash
# Windows
setup.bat

# Linux / macOS
chmod +x setup.sh
./setup.sh
```

The setup script will:
- Check for Python
- Install Poppler (with your permission)
- Create virtual environment
- Install all dependencies

**Then start the service:**

```bash
# Windows
start_local.bat

# Linux / macOS
./start_local.sh
```

📖 **Full installation guide:** [INSTALLATION.md](INSTALLATION.md)  
🔧 **Poppler troubleshooting:** [POPPLER_SETUP.md](POPPLER_SETUP.md)  
🐳 **Docker updates:** [DOCKER_UPDATE.md](DOCKER_UPDATE.md)

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
- Query Parameters (optional):
  - `output_format`: `base64` (default), `binary`, or `both`
  - `dpi`: Resolution (72-600, default: 200)

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

**Basic conversion (default settings):**
```bash
curl -X POST http://localhost:2277/api/v1/pdf-to-images \
  -H "x-api-key: your-secret-api-key" \
  -F "file=@sample.pdf"
```

**High-resolution conversion:**
```bash
curl -X POST "http://localhost:2277/api/v1/pdf-to-images?dpi=300&output_format=base64" \
  -H "x-api-key: your-secret-api-key" \
  -F "file=@sample.pdf"
```

📖 **Complete API documentation:** [API_USAGE.md](API_USAGE.md)

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

- Converts 5-page PDF in ~5 seconds (at 200 DPI)
- DPI: Configurable via API parameter (72-600, default: 200)
- Output format: JPEG
- Temporary files cleaned up after conversion
- Higher DPI values increase processing time and output size proportionally

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

