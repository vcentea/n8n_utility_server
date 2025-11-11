#!/usr/bin/env bash
set -euo pipefail

echo "========================================"
echo " Utility Service Platform Setup"
echo "========================================"
echo

# Detect OS
OS="$(uname -s)"
INSTALL_CMD=""

case "${OS}" in
    Linux*)
        if command -v apt-get &> /dev/null; then
            INSTALL_CMD="sudo apt-get install -y poppler-utils"
        elif command -v yum &> /dev/null; then
            INSTALL_CMD="sudo yum install -y poppler-utils"
        elif command -v dnf &> /dev/null; then
            INSTALL_CMD="sudo dnf install -y poppler-utils"
        fi
        ;;
    Darwin*)
        if command -v brew &> /dev/null; then
            INSTALL_CMD="brew install poppler"
        fi
        ;;
esac

# Check if .env exists
if [[ ! -f ".env" ]]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo
    echo "IMPORTANT: Edit .env and set your API_KEY before running!"
    echo
fi

# Check for Python
PYTHON_BIN=""
if command -v python3 &> /dev/null; then
    PYTHON_BIN="python3"
elif command -v python &> /dev/null; then
    PYTHON_BIN="python"
else
    echo "ERROR: Python is not installed!"
    echo "Please install Python 3.12+ first."
    exit 1
fi

echo "[1/4] Python found: $(${PYTHON_BIN} --version)"
echo

# Check for Poppler
echo "[2/4] Checking for Poppler..."
if ! command -v pdftoppm &> /dev/null; then
    echo
    echo "WARNING: Poppler is NOT installed!"
    echo "Poppler is REQUIRED for PDF conversion."
    echo
    
    if [[ -n "${INSTALL_CMD}" ]]; then
        echo "Detected install command: ${INSTALL_CMD}"
        echo
        read -p "Do you want to install Poppler now? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "Installing Poppler..."
            eval "${INSTALL_CMD}"
            
            if command -v pdftoppm &> /dev/null; then
                echo "Poppler installed successfully!"
            else
                echo "ERROR: Installation failed!"
                echo "Please install manually and run this setup again."
                exit 1
            fi
        else
            echo
            echo "Please install Poppler manually and run this setup again."
            echo "See POPPLER_SETUP.md for instructions."
            exit 1
        fi
    else
        echo "Could not detect package manager."
        echo "Please install Poppler manually:"
        echo
        case "${OS}" in
            Darwin*)
                echo "  brew install poppler"
                ;;
            *)
                echo "  See POPPLER_SETUP.md for instructions"
                ;;
        esac
        exit 1
    fi
else
    echo "Poppler found: $(which pdftoppm)"
fi
echo

# Create virtual environment
echo "[3/4] Setting up Python virtual environment..."
if [[ ! -d "venv" ]]; then
    "${PYTHON_BIN}" -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi
echo

# Install Python dependencies
echo "[4/4] Installing Python dependencies..."
# shellcheck source=/dev/null
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo

echo "========================================"
echo " Setup Complete!"
echo "========================================"
echo
echo "Next steps:"
echo "  1. Edit .env and set your API_KEY"
echo "  2. Run: ./start_local.sh"
echo
echo "For Docker deployment (zero configuration):"
echo "  docker-compose up -d"
echo

