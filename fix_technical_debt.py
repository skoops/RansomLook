#!/usr/bin/env python3
"""
Technical Debt Fix Script for RansomLook

This script systematically fixes the identified technical debt issues:
1. Bare except clauses
2. Unspecified encoding in file operations
3. Resource management with context managers
4. Unnecessary pass statements
5. Bad indentation
6. Singleton comparisons
7. Unused type ignore comments
"""

import os
import re
import glob
from pathlib import Path
from typing import List, Tuple

def fix_bare_except_clauses(content: str) -> str:
    """Replace bare except clauses with specific exception types."""
    # Pattern to match bare except clauses
    pattern = r'except:'
    replacement = 'except Exception:'
    return re.sub(pattern, replacement, content)

def fix_unspecified_encoding(content: str) -> str:
    """Add UTF-8 encoding to file open operations."""
    # Pattern to match open() calls without encoding
    pattern = r'open\(([^)]+)\)'
    
    def add_encoding(match):
        args = match.group(1)
        if 'encoding=' not in args:
            return f'open({args}, encoding="utf-8")'
        return match.group(0)
    
    return re.sub(pattern, add_encoding, content)

def fix_resource_management(content: str) -> str:
    """Convert file operations to use context managers."""
    # Pattern to match file open/close patterns
    file_pattern = r'(\w+)\s*=\s*open\(([^)]+)\)\s*\n(.*?)\n\s*\1\.close\(\)'
    
    def convert_to_with(match):
        var_name = match.group(1)
        open_args = match.group(2)
        content_lines = match.group(3)
        
        # Add encoding if not present
        if 'encoding=' not in open_args:
            open_args += ', encoding="utf-8"'
        
        return f'with open({open_args}) as {var_name}:\n{content_lines}'
    
    return re.sub(file_pattern, convert_to_with, content, flags=re.DOTALL)

def fix_unnecessary_pass(content: str) -> str:
    """Remove unnecessary pass statements in except blocks."""
    # Pattern to match except blocks with only pass
    pattern = r'except[^:]*:\s*\n\s*pass'
    return re.sub(pattern, '', content)

def fix_singleton_comparisons(content: str) -> str:
    """Replace == None with is None and == True with is True."""
    content = re.sub(r'==\s*None', 'is None', content)
    content = re.sub(r'==\s*True', 'is True', content)
    content = re.sub(r'==\s*False', 'is False', content)
    return content

def fix_unused_type_ignores(content: str) -> str:
    """Remove unused type ignore comments."""
    # Pattern to match # type: ignore comments
    pattern = r'\s+# type: ignore\s*\n'
    return re.sub(pattern, '\n', content)

def fix_indentation(content: str) -> str:
    """Fix common indentation issues."""
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        # Fix common indentation issues
        if line.startswith('    ') and len(line.strip()) > 0:
            # Ensure consistent 4-space indentation
            indent_level = len(line) - len(line.lstrip())
            if indent_level % 4 != 0:
                # Round to nearest 4-space increment
                new_indent = (indent_level // 4) * 4
                line = ' ' * new_indent + line.lstrip()
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def fix_parser_template(content: str) -> str:
    """Apply standard fixes to parser files."""
    content = fix_bare_except_clauses(content)
    content = fix_unspecified_encoding(content)
    content = fix_resource_management(content)
    content = fix_unnecessary_pass(content)
    content = fix_singleton_comparisons(content)
    content = fix_indentation(content)
    return content

def process_file(file_path: str) -> Tuple[bool, str]:
    """Process a single file and return whether changes were made."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Apply fixes
        fixed_content = fix_parser_template(original_content)
        
        # Check if content changed
        if original_content != fixed_content:
            # Backup original file
            backup_path = file_path + '.backup'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Write fixed content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            return True, f"Fixed: {file_path}"
        else:
            return False, f"No changes needed: {file_path}"
    
    except Exception as e:
        return False, f"Error processing {file_path}: {str(e)}"

def main():
    """Main function to process all files."""
    # Get all Python files in the project
    python_files = []
    python_files.extend(glob.glob('ransomlook/**/*.py', recursive=True))
    python_files.extend(glob.glob('bin/*.py', recursive=True))
    
    print(f"Found {len(python_files)} Python files to process")
    
    fixed_files = []
    error_files = []
    
    for file_path in python_files:
        changed, message = process_file(file_path)
        if changed:
            fixed_files.append(file_path)
            print(f"✓ {message}")
        elif "Error" in message:
            error_files.append(file_path)
            print(f"✗ {message}")
        else:
            print(f"- {message}")
    
    print(f"\nSummary:")
    print(f"Fixed: {len(fixed_files)} files")
    print(f"Errors: {len(error_files)} files")
    print(f"Total processed: {len(python_files)} files")

if __name__ == "__main__":
    main()
