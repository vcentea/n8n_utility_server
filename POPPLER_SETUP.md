# Poppler Setup Guide

## What is Poppler?

Poppler is a PDF rendering library (written in C/C++, not Python). The `pdf2image` Python package is just a wrapper that calls Poppler's command-line tools to convert PDFs to images.

**Think of it like this:**
- `pdf2image` = the steering wheel
- `Poppler` = the engine

You need both!

## Installation by Platform

### Windows (Choose One Method)

#### Option 1: Chocolatey (Easiest)
```cmd
choco install poppler
```

#### Option 2: Manual Download
1. Download Poppler for Windows: https://github.com/oschwartz10612/poppler-windows/releases
2. Download the latest release ZIP (e.g., `Release-XX.XX.X-X.zip`)
3. Extract to a simple location like `C:\poppler`
4. The binaries will be in `C:\poppler\Library\bin`

**Auto-Detection:**
The application automatically checks these locations:
- `C:\Program Files\poppler\Library\bin`
- `C:\Program Files (x86)\poppler\Library\bin`
- `C:\poppler\Library\bin`
- `C:\poppler\bin`
- `%USERPROFILE%\poppler\Library\bin`
- `%USERPROFILE%\poppler\bin`

If you install to one of these locations, you don't need to set `POPPLER_PATH`!

#### Option 3: Add to System PATH
1. Download and extract Poppler as above
2. Add `C:\poppler\Library\bin` to your System PATH:
   - Right-click "This PC" → Properties → Advanced system settings
   - Environment Variables → System variables → Path → Edit
   - Add new entry: `C:\poppler\Library\bin`
   - Restart your terminal/IDE

### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install -y poppler-utils
```

**No configuration needed!** Poppler is automatically in PATH.

### Linux (CentOS/RHEL)
```bash
sudo yum install -y poppler-utils
```

### macOS
```bash
brew install poppler
```

**No configuration needed!** Poppler is automatically in PATH.

## Verification

Check if Poppler is installed and accessible:

### Windows
```cmd
where pdftoppm
```

### Linux/macOS
```bash
which pdftoppm
```

If you see a path, Poppler is installed correctly!

## Configuration (Only if needed)

If Poppler is **not** in PATH and **not** in a common location, set `POPPLER_PATH` in your `.env` file:

```
POPPLER_PATH=C:\path\to\poppler\Library\bin
```

**Note:** Point to the directory containing `pdftoppm.exe` (Windows) or `pdftoppm` (Linux/macOS).

## Docker

**No setup needed!** The Docker image includes Poppler automatically via:
```dockerfile
RUN apk add --no-cache poppler-utils
```

## Troubleshooting

### Error: "Poppler is not installed or POPPLER_PATH is incorrect"

**On Windows:**
1. Download Poppler from the link above
2. Extract to `C:\poppler`
3. Verify `C:\poppler\Library\bin\pdftoppm.exe` exists
4. Either:
   - Restart your application (auto-detection will find it)
   - OR add to System PATH
   - OR set `POPPLER_PATH=C:\poppler\Library\bin` in `.env`

**On Linux/macOS:**
```bash
sudo apt-get install poppler-utils  # Ubuntu/Debian
brew install poppler                # macOS
```

### Check Auto-Detection (Windows)

Run this Python script to see what the app detects:
```python
import os
import platform
from pathlib import Path

def find_poppler_path():
    if platform.system() != "Windows":
        print("Linux/macOS: Poppler should be in PATH")
        return ""
    
    common_locations = [
        Path("C:/Program Files/poppler/Library/bin"),
        Path("C:/Program Files (x86)/poppler/Library/bin"),
        Path("C:/poppler/Library/bin"),
        Path("C:/poppler/bin"),
        Path.home() / "poppler/Library/bin",
        Path.home() / "poppler/bin",
    ]
    
    for location in common_locations:
        if location.exists() and (location / "pdftoppm.exe").exists():
            print(f"✓ Found Poppler at: {location}")
            return str(location)
    
    print("✗ Poppler not found in common locations")
    return ""

print(f"Platform: {platform.system()}")
result = find_poppler_path()
if result:
    print(f"Auto-detected: {result}")
else:
    print("You need to install Poppler or set POPPLER_PATH")
```

## Quick Start Summary

| Platform | Command | Config Needed? |
|----------|---------|----------------|
| **Windows** (Choco) | `choco install poppler` | Maybe (if not in PATH) |
| **Windows** (Manual) | Extract to `C:\poppler` | No (auto-detected) |
| **Ubuntu/Debian** | `sudo apt-get install poppler-utils` | No |
| **macOS** | `brew install poppler` | No |
| **Docker** | Nothing (included) | No |

## Why Not Bundle Poppler with Python?

Good question! Poppler is a large C/C++ library with system dependencies. Bundling it would:
- Make the Python package huge (50+ MB)
- Require separate builds for each OS/architecture
- Complicate licensing

Instead, it's installed system-wide (like a database or web server) and shared by all apps.

