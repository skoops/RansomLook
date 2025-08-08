#!/usr/bin/env python3
"""
Remove unused type ignore comments

This script removes the unused type ignore comments identified by mypy.
"""

import re
import glob
from pathlib import Path

def remove_unused_type_ignores(content: str) -> str:
    """Remove unused type ignore comments."""
    # Pattern to match # type: ignore comments
    pattern = r'\s+# type: ignore\s*\n'
    return re.sub(pattern, '\n', content)

def process_files():
    """Process files with unused type ignores."""
    # Files identified by mypy with unused type ignores
    files_to_fix = [
        'ransomlook/sharedutils.py',
        'ransomlook/twitter.py', 
        'ransomlook/telegram.py',
        'ransomlook/rocket.py',
        'ransomlook/mastodon.py',
        'ransomlook/ransomlook.py'
    ]
    
    fixed_count = 0
    for file_path in files_to_fix:
        if Path(file_path).exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    original_content = f.read()
                
                fixed_content = remove_unused_type_ignores(original_content)
                
                if original_content != fixed_content:
                    # Create backup
                    backup_file = file_path + '.backup'
                    with open(backup_file, 'w', encoding='utf-8') as f:
                        f.write(original_content)
                    
                    # Write fixed content
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(fixed_content)
                    
                    print(f"✓ Fixed: {file_path}")
                    fixed_count += 1
                else:
                    print(f"- No changes: {file_path}")
                    
            except Exception as e:
                print(f"✗ Error processing {file_path}: {e}")
        else:
            print(f"✗ File not found: {file_path}")
    
    print(f"\nFixed {fixed_count} files")

if __name__ == "__main__":
    process_files()
