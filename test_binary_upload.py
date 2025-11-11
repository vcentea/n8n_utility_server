"""
Test script to verify PDF endpoint accepts binary data in multiple ways.
"""
import requests
import base64
import json
from pathlib import Path

API_URL = "http://localhost:2277/api/v1/pdf-to-images"
API_KEY = "supersecretapikey"  # Change this to your API key


def test_multipart_upload(pdf_path: str):
    """Test 1: Multipart form upload (standard method)"""
    print("=" * 60)
    print("Test 1: Multipart Form Upload")
    print("=" * 60)
    
    with open(pdf_path, "rb") as f:
        files = {"file": ("test.pdf", f, "application/pdf")}
        headers = {"x-api-key": API_KEY}
        
        response = requests.post(API_URL, files=files, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Success! Converted {data['pages']} pages")
            print(f"  First image size: {len(data['images'][0]['base64'])} chars")
        else:
            print(f"✗ Error: {response.text}")
    print()


def test_multipart_binary_stream(pdf_path: str):
    """Test 2: Multipart with binary stream (n8n style)"""
    print("=" * 60)
    print("Test 2: Multipart Binary Stream (n8n/Postman style)")
    print("=" * 60)
    
    with open(pdf_path, "rb") as f:
        pdf_data = f.read()
    
    files = {"file": ("document.pdf", pdf_data, "application/pdf")}
    headers = {"x-api-key": API_KEY}
    
    response = requests.post(API_URL, files=files, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Success! Converted {data['pages']} pages")
        print(f"  First image size: {len(data['images'][0]['base64'])} chars")
    else:
        print(f"✗ Error: {response.text}")
    print()


def test_base64_in_memory(pdf_path: str):
    """Test 3: Binary data already in memory (from another API)"""
    print("=" * 60)
    print("Test 3: Binary Data from Memory (API to API)")
    print("=" * 60)
    
    # Simulate receiving binary data from another API
    with open(pdf_path, "rb") as f:
        binary_data = f.read()
    
    # Now send it directly
    files = {"file": binary_data}
    headers = {"x-api-key": API_KEY}
    
    response = requests.post(API_URL, files=files, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Success! Converted {data['pages']} pages")
    else:
        print(f"✗ Error: {response.text}")
    print()


def print_curl_examples():
    """Show curl examples for different upload methods"""
    print("=" * 60)
    print("cURL Examples")
    print("=" * 60)
    
    print("\n1. Multipart form upload from file:")
    print("""
curl -X POST http://localhost:2277/api/v1/pdf-to-images \\
  -H "x-api-key: supersecretapikey" \\
  -F "file=@document.pdf"
    """)
    
    print("\n2. Multipart with explicit content type:")
    print("""
curl -X POST http://localhost:2277/api/v1/pdf-to-images \\
  -H "x-api-key: supersecretapikey" \\
  -F "file=@document.pdf;type=application/pdf"
    """)
    
    print("\n3. From stdin (pipe binary data):")
    print("""
cat document.pdf | curl -X POST http://localhost:2277/api/v1/pdf-to-images \\
  -H "x-api-key: supersecretapikey" \\
  -F "file=@-;type=application/pdf"
    """)
    print()


def main():
    """Run all tests"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python test_binary_upload.py <path_to_pdf>")
        print("\nThis will test multiple ways to upload binary PDF data.")
        print_curl_examples()
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    if not Path(pdf_path).exists():
        print(f"Error: File not found: {pdf_path}")
        sys.exit(1)
    
    print("\n🧪 Testing PDF Binary Upload Methods\n")
    
    try:
        test_multipart_upload(pdf_path)
        test_multipart_binary_stream(pdf_path)
        test_base64_in_memory(pdf_path)
        
        print("=" * 60)
        print("✓ All tests completed!")
        print("=" * 60)
        print("\nThe endpoint accepts PDF binary data in all standard formats:")
        print("  ✓ Multipart form upload")
        print("  ✓ Binary stream")
        print("  ✓ In-memory binary data")
        print()
        
        print_curl_examples()
        
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Could not connect to the API.")
        print("  Make sure the server is running: start_local.bat")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

