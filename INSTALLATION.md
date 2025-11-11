# Installation Guide

## Choose Your Deployment Method

### 🐳 Docker (Recommended - Zero Configuration)

**Everything is automatic!** Poppler is included in the Docker image.

```bash
# 1. Create .env file
cp .env.example .env
# Edit .env and set your API_KEY

# 2. Start the service
docker-compose up -d

# 3. Done! Service is running on port 2277
```

✅ **Works out of the box**  
✅ **Poppler automatically installed**  
✅ **No manual dependencies**  
✅ **Same on all platforms**

---

### 💻 Local Development

Requires **manual setup** of Poppler + Python dependencies.

#### Windows

**Option A: Automated Setup (Recommended)**
```cmd
# Run the setup script
setup.bat
```

The script will:
- ✅ Create `.env` file
- ✅ Check for Python
- ✅ Offer to install Poppler via Chocolatey
- ✅ Create virtual environment
- ✅ Install Python dependencies

**Option B: Manual Setup**
1. Install Python 3.12+
2. Install Poppler:
   - Via Chocolatey: `choco install poppler`
   - OR download and extract to `C:\poppler`: https://github.com/oschwartz10612/poppler-windows/releases
3. Run:
   ```cmd
   copy .env.example .env
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

#### Linux

**Option A: Automated Setup (Recommended)**
```bash
# Make executable and run
chmod +x setup.sh
./setup.sh
```

The script will:
- ✅ Create `.env` file
- ✅ Check for Python
- ✅ Offer to install Poppler automatically
- ✅ Create virtual environment
- ✅ Install Python dependencies

**Option B: Manual Setup**
```bash
# 1. Install Poppler
sudo apt-get update
sudo apt-get install -y poppler-utils  # Ubuntu/Debian
# OR
sudo yum install -y poppler-utils      # CentOS/RHEL

# 2. Setup Python environment
cp .env.example .env
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### macOS

**Option A: Automated Setup (Recommended)**
```bash
# Make executable and run
chmod +x setup.sh
./setup.sh
```

**Option B: Manual Setup**
```bash
# 1. Install Poppler
brew install poppler

# 2. Setup Python environment
cp .env.example .env
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Comparison Table

| Method | Poppler Installation | Python Dependencies | Configuration |
|--------|---------------------|---------------------|---------------|
| **Docker** | ✅ Automatic | ✅ Automatic | Minimal (.env only) |
| **Local - Automated Setup** | 🟡 Prompted/Guided | ✅ Automatic | Minimal (.env only) |
| **Local - Manual Setup** | ❌ Manual | ❌ Manual | Manual (.env + deps) |

---

## Running the Service

### Docker
```bash
docker-compose up -d           # Start
docker-compose logs -f         # View logs
docker-compose down            # Stop
```

### Local Development

**Windows:**
```cmd
start_local.bat
```

**Linux/macOS:**
```bash
chmod +x start_local.sh
./start_local.sh
```

---

## Verification

Test that everything works:

```bash
# Test the health endpoint
curl http://localhost:2277/health

# Should return: {"status":"healthy"}
```

Test PDF conversion:

**Windows:**
```cmd
test_endpoint.bat
```

**Linux/macOS:**
```bash
chmod +x test_endpoint.sh
./test_endpoint.sh
```

---

## Quick Reference

### Docker (Production - Easiest)
```bash
cp .env.example .env              # Configure
docker-compose up -d              # Start
curl http://localhost:2277/health # Test
```

### Local Windows (Development)
```cmd
setup.bat              # One-time setup
start_local.bat        # Start server
test_endpoint.bat      # Test conversion
```

### Local Linux/macOS (Development)
```bash
chmod +x setup.sh start_local.sh test_endpoint.sh
./setup.sh             # One-time setup
./start_local.sh       # Start server
./test_endpoint.sh     # Test conversion
```

---

## Troubleshooting

### Poppler Not Found
- **Docker**: This shouldn't happen (it's included)
- **Local**: Run `setup.bat` or `setup.sh` to install
- **Manual**: See [POPPLER_SETUP.md](POPPLER_SETUP.md)

### Python Not Found
Install Python 3.12+ from:
- Windows: https://www.python.org/downloads/
- Linux: `sudo apt-get install python3`
- macOS: `brew install python@3.12`

### Port Already in Use
Change `PORT=2277` to another port in your `.env` file.

### Permission Denied (Linux/macOS)
```bash
chmod +x setup.sh start_local.sh test_endpoint.sh
```

---

## Why Docker is Recommended

1. **Zero Configuration**: No manual dependency installation
2. **Consistent**: Same environment everywhere
3. **Isolated**: Doesn't affect your system
4. **Easy Updates**: `docker-compose pull && docker-compose up -d`
5. **Production Ready**: Deploy the same image everywhere

For production deployments, **always use Docker**.

