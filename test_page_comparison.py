"""
Diagnostic script to check if PDF pages are actually different.
This will help identify if pages are truly duplicated or just visually similar.
"""
import requests
import sys
from pathlib import Path

API_URL = "http://localhost:2277/api/v1/pdf-to-images"
API_KEY = "supersecretapikey"


def analyze_pages(pdf_path: str):
    """Analyze PDF pages to check for duplicates"""
    print("=" * 80)
    print("PDF Page Duplication Diagnostic")
    print("=" * 80)
    
    with open(pdf_path, "rb") as f:
        files = {"file": ("test.pdf", f, "application/pdf")}
        headers = {"x-api-key": API_KEY}
        params = {"output_format": "base64"}
        
        response = requests.post(API_URL, files=files, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"✗ Error: {response.text}")
            return
        
        data = response.json()
        total_pages = data['pages']
        images = data['images']
        
        print(f"\n✓ Successfully converted {total_pages} pages\n")
        
        # Analyze each page
        print("Page Analysis:")
        print("-" * 80)
        print(f"{'Page':<6} {'Filename':<15} {'Width':<8} {'Height':<8} {'Mode':<6} {'Size (KB)':<12}")
        print("-" * 80)
        
        seen_hashes = {}
        duplicates = []
        
        for img in images:
            page_num = img['page']
            filename = img['file_name']
            width = img['width']
            height = img['height']
            mode = img['mode']
            size_kb = img['size_bytes'] / 1024
            base64_data = img['base64']
            
            # Create a hash of the base64 data to check for exact duplicates
            import hashlib
            data_hash = hashlib.md5(base64_data.encode()).hexdigest()
            
            print(f"{page_num:<6} {filename:<15} {width:<8} {height:<8} {mode:<6} {size_kb:<12.2f}")
            
            # Check for duplicates
            if data_hash in seen_hashes:
                duplicates.append({
                    'current': page_num,
                    'duplicate_of': seen_hashes[data_hash],
                    'hash': data_hash[:8]
                })
            else:
                seen_hashes[data_hash] = page_num
        
        print("-" * 80)
        
        # Report findings
        print(f"\n{'Analysis Results:':^80}")
        print("=" * 80)
        
        if duplicates:
            print(f"\n⚠ DUPLICATES FOUND: {len(duplicates)} page(s)")
            print("\nDuplicate pages (exact binary match):")
            for dup in duplicates:
                print(f"  • Page {dup['current']} is identical to Page {dup['duplicate_of']}")
                print(f"    Hash: {dup['hash']}...")
            print("\n✗ This indicates a bug in the PDF conversion process!")
        else:
            print(f"\n✓ NO DUPLICATES: All {total_pages} pages are unique")
            print("\nIf pages look visually similar, it might be:")
            print("  • The invoice pages actually have similar content")
            print("  • Headers/footers are the same across pages")
            print("  • You're viewing cached images")
            
        # Size analysis
        print("\nSize Analysis:")
        sizes = [img['size_bytes'] for img in images]
        avg_size = sum(sizes) / len(sizes)
        print(f"  Average page size: {avg_size/1024:.2f} KB")
        print(f"  Smallest page: {min(sizes)/1024:.2f} KB (Page {sizes.index(min(sizes))+1})")
        print(f"  Largest page: {max(sizes)/1024:.2f} KB (Page {sizes.index(max(sizes))+1})")
        
        # Dimension analysis
        dimensions = [(img['width'], img['height']) for img in images]
        unique_dimensions = set(dimensions)
        print(f"\nDimension Analysis:")
        print(f"  Unique dimensions: {len(unique_dimensions)}")
        for dim in unique_dimensions:
            count = dimensions.count(dim)
            print(f"    {dim[0]}x{dim[1]}: {count} page(s)")
        
        print("\n" + "=" * 80)


def main():
    """Run diagnostic"""
    if len(sys.argv) < 2:
        print("Usage: python test_page_comparison.py <path_to_pdf>")
        print("\nThis will analyze each page to detect if pages are truly duplicated")
        print("or just visually similar.")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    if not Path(pdf_path).exists():
        print(f"Error: File not found: {pdf_path}")
        sys.exit(1)
    
    try:
        analyze_pages(pdf_path)
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



