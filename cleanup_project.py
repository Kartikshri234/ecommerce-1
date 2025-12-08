import os
import shutil
from pathlib import Path

# Base directory
BASE_DIR = Path(r"C:\Users\karti\OneDrive\Desktop\claude")

def cleanup_project():
    """
    Cleanup and reorganize Django project structure
    """
    
    print("=" * 60)
    print("DJANGO PROJECT CLEANUP SCRIPT")
    print("=" * 60)
    
    # Track what we're doing
    items_to_delete = []
    items_to_keep = []
    
    # 1. Remove duplicate root-level directories (keep only in ecommerce/)
    print("\n1. Removing duplicate root-level directories...")
    duplicates = ['shop', 'static', 'templates', 'media']
    
    for folder in duplicates:
        root_path = BASE_DIR / folder
        if root_path.exists():
            items_to_delete.append(str(root_path))
            print(f"   ❌ Will delete: {root_path} (duplicate)")
    
    # 2. Remove duplicate database file
    print("\n2. Checking database files...")
    root_db = BASE_DIR / "db.sqlite3"
    ecommerce_db = BASE_DIR / "ecommerce" / "db.sqlite3"
    
    if root_db.exists() and ecommerce_db.exists():
        items_to_delete.append(str(root_db))
        print(f"   ❌ Will delete: {root_db} (keeping ecommerce/db.sqlite3)")
        items_to_keep.append(str(ecommerce_db))
    elif root_db.exists():
        items_to_keep.append(str(root_db))
        print(f"   ✅ Keeping: {root_db}")
    
    # 3. Remove all __pycache__ directories
    print("\n3. Finding Python cache directories...")
    pycache_dirs = list(BASE_DIR.rglob("__pycache__"))
    for cache_dir in pycache_dirs:
        items_to_delete.append(str(cache_dir))
    print(f"   ❌ Found {len(pycache_dirs)} __pycache__ directories to delete")
    
    # 4. Remove duplicate .hintrc files
    print("\n4. Checking .hintrc files...")
    root_hintrc = BASE_DIR / ".hintrc"
    ecommerce_hintrc = BASE_DIR / "ecommerce" / ".hintrc"
    
    if root_hintrc.exists() and ecommerce_hintrc.exists():
        items_to_delete.append(str(ecommerce_hintrc))
        print(f"   ❌ Will delete: {ecommerce_hintrc} (keeping root .hintrc)")
    
    # 5. Clean duplicate media files
    print("\n5. Analyzing media directory for duplicates...")
    media_dir = BASE_DIR / "ecommerce" / "media" / "product_images"
    if media_dir.exists():
        duplicate_images = []
        for img in media_dir.glob("*_*.jpg"):
            # Files with suffixes like _7kDsZhL.jpg are duplicates
            if any(suffix in img.name for suffix in ['_7kDsZhL', '_B1Zj1fn', '_dA68wkw', 
                                                       '_DrN1be2', '_dAA5MKH', '_jiSRMAR', 
                                                       '_tTw4pTe', '_Z8IZUpR', '_8LWvAji', 
                                                       '_g7oi9vY', '_rbETIXm', '_SgqHqx8']):
                duplicate_images.append(img)
                items_to_delete.append(str(img))
        
        print(f"   ❌ Found {len(duplicate_images)} duplicate product images")
    
    # 6. Check for empty directories
    print("\n6. Checking for empty directories...")
    empty_dirs = []
    docs_dir = BASE_DIR / "docs"
    if docs_dir.exists() and not any(docs_dir.iterdir()):
        empty_dirs.append(docs_dir)
        items_to_delete.append(str(docs_dir))
    
    if empty_dirs:
        print(f"   ❌ Found {len(empty_dirs)} empty directories")
    
    # Summary
    print("\n" + "=" * 60)
    print("CLEANUP SUMMARY")
    print("=" * 60)
    print(f"\nTotal items to delete: {len(items_to_delete)}")
    print(f"Total items to keep: {len(items_to_keep)}")
    
    # Calculate space savings (approximate)
    total_size = 0
    for item in items_to_delete:
        item_path = Path(item)
        if item_path.exists():
            if item_path.is_file():
                total_size += item_path.stat().st_size
            elif item_path.is_dir():
                for file in item_path.rglob("*"):
                    if file.is_file():
                        total_size += file.stat().st_size
    
    print(f"\nEstimated space to be freed: {total_size / (1024*1024):.2f} MB")
    
    # Ask for confirmation
    print("\n" + "=" * 60)
    response = input("\nDo you want to proceed with deletion? (yes/no): ").strip().lower()
    
    if response == 'yes':
        print("\n🚀 Starting cleanup...")
        
        deleted_count = 0
        error_count = 0
        
        for item in items_to_delete:
            item_path = Path(item)
            try:
                if item_path.exists():
                    if item_path.is_dir():
                        shutil.rmtree(item_path)
                    else:
                        item_path.unlink()
                    deleted_count += 1
                    print(f"   ✅ Deleted: {item_path.name}")
            except Exception as e:
                error_count += 1
                print(f"   ❌ Error deleting {item_path.name}: {str(e)}")
        
        print(f"\n✨ Cleanup complete!")
        print(f"   - Deleted: {deleted_count} items")
        print(f"   - Errors: {error_count} items")
        print(f"   - Space freed: {total_size / (1024*1024):.2f} MB")
    else:
        print("\n❌ Cleanup cancelled. No files were deleted.")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    try:
        cleanup_project()
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        print("Please check the script and try again.")