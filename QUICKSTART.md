# Quick Start Guide

## Local Development (Windows)

1. **Setup Environment:**
```cmd
copy .env.example .env
```

2. **Edit .env and set your API_KEY:**
```
API_KEY=your-secret-key-here
```

3. **Download and install poppler:**
   - Download from: https://github.com/oschwartz10612/poppler-windows/releases
   - Extract and set the `POPPLER_PATH` value in `.env` (e.g. `C:\poppler\Library\bin`)

4. **Run the service:**
```cmd
start_local.bat
```

5. **Test the endpoint:**
```cmd
test_endpoint.bat
```

Or test manually:
```cmd
curl -X POST http://localhost:2277/api/v1/pdf-to-images ^
  -H "x-api-key: your-secret-key-here" ^
  -F "file=@test.pdf"
```

## Local Development (Linux / macOS)

1. **Setup Environment:**
```bash
cp .env.example .env
```

2. **Edit `.env` and set values:**
```bash
API_KEY=your-secret-key-here
POPPLER_PATH=/usr/local/bin  # optional if Poppler is not in PATH
```

3. **Install poppler-utils:**
```bash
# Ubuntu / Debian
sudo apt-get install poppler-utils

# macOS (Homebrew)
brew install poppler
```

4. **Run the service:**
```bash
chmod +x start_local.sh
./start_local.sh
```

5. **Test the endpoint:**
```bash
chmod +x test_endpoint.sh
./test_endpoint.sh
```

Or manually:
```bash
curl -X POST http://localhost:2277/api/v1/pdf-to-images \
  -H "x-api-key: your-secret-key-here" \
  -F "file=@test.pdf"
```

## Docker Deployment

1. **Create .env file:**
```cmd
copy .env.example .env
```

2. **Build and run with Docker Compose:**
```cmd
docker-compose up -d
```

3. **View logs:**
```cmd
docker-compose logs -f
```

4. **Stop the service:**
```cmd
docker-compose down
```

## Testing

Access the API documentation at: http://localhost:2277/docs

## Production Deployment (Ubuntu)

1. **Clone repository:**
```bash
git clone <your-repo>
cd utility-service
```

2. **Configure environment:**
```bash
cp .env.example .env
nano .env  # Set your API_KEY
```

3. **Deploy with Docker:**
```bash
docker-compose up -d
```

4. **Monitor:**
```bash
docker-compose logs -f utility-service
```

## Example n8n Integration

1. Add HTTP Request node
2. Set method: `POST`
3. URL: `http://your-server:2277/api/v1/pdf-to-images`
4. Add header: `x-api-key` = `your-secret-key-here`
5. Body Content Type: `Form-Data Multipart`
6. Specify Input Binary Field with your PDF

