"""
Test script to verify different output formats.
"""
import requests
import base64
import sys
from pathlib import Path

API_URL = "http://localhost:2277/api/v1/pdf-to-images"
API_KEY = "supersecretapikey"


def test_format(pdf_path: str, output_format: str):
    """Test specific output format"""
    print(f"\n{'='*60}")
    print(f"Testing output_format='{output_format}'")
    print('='*60)
    
    with open(pdf_path, "rb") as f:
        files = {"file": ("test.pdf", f, "application/pdf")}
        headers = {"x-api-key": API_KEY}
        params = {"output_format": output_format}
        
        response = requests.post(API_URL, files=files, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"✗ Error: {response.text}")
            return
        
        data = response.json()
        print(f"✓ Success! Converted {data['pages']} pages")
        
        first_image = data['images'][0]
        print(f"\nFirst page contains:")
        print(f"  - page: {first_image.get('page')}")
        print(f"  - file_name: {first_image.get('file_name')}")
        
        if 'base64' in first_image:
            print(f"  - base64: {len(first_image['base64'])} characters")
            print(f"    Preview: {first_image['base64'][:50]}...")
            
            # Verify base64 is valid
            try:
                img_bytes = base64.b64decode(first_image['base64'])
                print(f"    ✓ Valid base64 (decoded to {len(img_bytes)} bytes)")
            except Exception as e:
                print(f"    ✗ Invalid base64: {e}")
        
        if 'binary' in first_image:
            print(f"  - binary: {len(first_image['binary'])} bytes as array")
            print(f"    First 10 bytes: {first_image['binary'][:10]}")
            
            # Verify JPEG signature
            if first_image['binary'][:2] == [0xFF, 0xD8]:
                print(f"    ✓ Valid JPEG signature")
            else:
                print(f"    ✗ Invalid JPEG signature")
        
        # Calculate response size
        import json
        response_size = len(json.dumps(data))
        print(f"\nResponse size: {response_size:,} bytes ({response_size/1024:.1f} KB)")


def save_image_example(pdf_path: str):
    """Example: Save images from different formats"""
    print(f"\n{'='*60}")
    print("Example: Saving Images from Different Formats")
    print('='*60)
    
    output_dir = Path("output_test")
    output_dir.mkdir(exist_ok=True)
    
    # Test base64 format
    with open(pdf_path, "rb") as f:
        files = {"file": ("test.pdf", f, "application/pdf")}
        headers = {"x-api-key": API_KEY}
        params = {"output_format": "base64"}
        
        response = requests.post(API_URL, files=files, headers=headers, params=params)
        data = response.json()
        
        for img in data['images']:
            img_bytes = base64.b64decode(img['base64'])
            output_path = output_dir / f"base64_{img['file_name']}"
            output_path.write_bytes(img_bytes)
            print(f"✓ Saved: {output_path} ({len(img_bytes)} bytes)")
    
    # Test binary format
    with open(pdf_path, "rb") as f:
        files = {"file": ("test.pdf", f, "application/pdf")}
        headers = {"x-api-key": API_KEY}
        params = {"output_format": "binary"}
        
        response = requests.post(API_URL, files=files, headers=headers, params=params)
        data = response.json()
        
        for img in data['images']:
            img_bytes = bytes(img['binary'])
            output_path = output_dir / f"binary_{img['file_name']}"
            output_path.write_bytes(img_bytes)
            print(f"✓ Saved: {output_path} ({len(img_bytes)} bytes)")
    
    print(f"\n✓ All images saved to: {output_dir.absolute()}")


def print_usage_examples():
    """Print cURL examples for different formats"""
    print(f"\n{'='*60}")
    print("cURL Usage Examples")
    print('='*60)
    
    print("\n1. Base64 format (default):")
    print("""
curl -X POST "http://localhost:2277/api/v1/pdf-to-images?output_format=base64" \\
  -H "x-api-key: supersecretapikey" \\
  -F "file=@document.pdf"
    """)
    
    print("\n2. Binary format (raw JPEG bytes as array):")
    print("""
curl -X POST "http://localhost:2277/api/v1/pdf-to-images?output_format=binary" \\
  -H "x-api-key: supersecretapikey" \\
  -F "file=@document.pdf"
    """)
    
    print("\n3. Both formats:")
    print("""
curl -X POST "http://localhost:2277/api/v1/pdf-to-images?output_format=both" \\
  -H "x-api-key: supersecretapikey" \\
  -F "file=@document.pdf"
    """)
    
    print("\n4. Default (no parameter, uses base64):")
    print("""
curl -X POST "http://localhost:2277/api/v1/pdf-to-images" \\
  -H "x-api-key: supersecretapikey" \\
  -F "file=@document.pdf"
    """)


def main():
    """Run all tests"""
    if len(sys.argv) < 2:
        print("Usage: python test_output_formats.py <path_to_pdf>")
        print("\nThis will test all output format options.")
        print_usage_examples()
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    if not Path(pdf_path).exists():
        print(f"Error: File not found: {pdf_path}")
        sys.exit(1)
    
    print("\n🧪 Testing PDF Output Formats\n")
    
    try:
        # Test each format
        test_format(pdf_path, "base64")
        test_format(pdf_path, "binary")
        test_format(pdf_path, "both")
        
        # Save examples
        save_image_example(pdf_path)
        
        print(f"\n{'='*60}")
        print("✓ All tests completed!")
        print('='*60)
        
        print("\nOutput formats available:")
        print("  ✓ base64  - Base64-encoded JPEG (default)")
        print("  ✓ binary  - Raw JPEG bytes as array")
        print("  ✓ both    - Both base64 and binary")
        
        print_usage_examples()
        
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Could not connect to the API.")
        print("  Make sure the server is running: start_local.bat")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

