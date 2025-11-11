# Quick Start Guide

## 🐳 Docker (Recommended - Works Out of the Box)

**Zero configuration needed - Poppler included automatically!**

```bash
# 1. Create and configure .env
cp .env.example .env
# Edit .env and set your API_KEY

# 2. Start the service
docker-compose up -d

# 3. Test it
curl http://localhost:2277/health

# 4. View logs
docker-compose logs -f

# 5. Stop
docker-compose down
```

**That's it!** No Poppler installation, no dependencies to manage.

---

## 💻 Local Development

### Windows

```cmd
REM 1. Run setup (installs everything)
setup.bat

REM 2. Edit .env and set your API_KEY

REM 3. Start the service
start_local.bat

REM 4. Test the endpoint
test_endpoint.bat
```

### Linux / macOS

```bash
# 1. Run setup (installs everything)
chmod +x setup.sh
./setup.sh

# 2. Edit .env and set your API_KEY

# 3. Start the service
chmod +x start_local.sh
./start_local.sh

# 4. Test the endpoint
chmod +x test_endpoint.sh
./test_endpoint.sh
```

---

## API Documentation

Access interactive docs at: http://localhost:2277/docs

---

## Production Deployment (Docker on Ubuntu)

```bash
# 1. Clone repository
git clone https://github.com/vcentea/n8n_utility_server.git
cd n8n_utility_server

# 2. Configure
cp .env.example .env
nano .env  # Set your API_KEY

# 3. Start with Docker Compose
docker-compose up -d

# 4. Verify
curl http://localhost:2277/health

# 5. Monitor logs
docker-compose logs -f
```

---

## Test the API

### Using cURL

```bash
curl -X POST http://localhost:2277/api/v1/pdf-to-images \
  -H "x-api-key: your-secret-key-here" \
  -F "file=@/path/to/your.pdf"
```

### Using the Test Script

**Windows:**
```cmd
test_endpoint.bat
```

**Linux/macOS:**
```bash
./test_endpoint.sh
```

---

## n8n Integration

1. Add **HTTP Request** node
2. Configure:
   - **Method**: `POST`
   - **URL**: `http://your-server:2277/api/v1/pdf-to-images`
   - **Authentication**: None
   - **Send Headers**: Yes
     - Name: `x-api-key`
     - Value: `your-secret-key-here`
   - **Send Body**: Yes
     - Content Type: `Form-Data Multipart`
     - Specify Binary Property with your PDF file

3. The response will contain base64-encoded images for each PDF page

---

## Key Differences

| Feature | Docker | Local Development |
|---------|--------|-------------------|
| **Poppler** | ✅ Auto-included | ❌ Manual install |
| **Setup Time** | < 2 minutes | ~5 minutes |
| **Dependencies** | None | Python, Poppler |
| **Updates** | `docker-compose pull` | `git pull` + reinstall |
| **Production Ready** | ✅ Yes | 🟡 Not recommended |

**For production, always use Docker!**
