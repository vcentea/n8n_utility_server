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

3. **Install Python dependencies:**
```cmd
pip install -r requirements.txt
```

4. **Download and install poppler:**
   - Download from: https://github.com/oschwartz10612/poppler-windows/releases
   - Extract and add to PATH

5. **Run the service:**
```cmd
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

6. **Test the endpoint:**
```cmd
curl -X POST http://localhost:8080/api/v1/pdf-to-images ^
  -H "x-api-key: your-secret-key-here" ^
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

Access the API documentation at: http://localhost:8080/docs

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
3. URL: `http://your-server:8080/api/v1/pdf-to-images`
4. Add header: `x-api-key` = `your-secret-key-here`
5. Body Content Type: `Form-Data Multipart`
6. Specify Input Binary Field with your PDF

