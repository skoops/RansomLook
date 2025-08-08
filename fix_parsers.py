#!/usr/bin/env python3
"""
Parser Files Technical Debt Fix Script

This script specifically targets the common issues found in the parser files:
1. Bare except clauses
2. Unspecified encoding in file operations
3. Resource management with context managers
4. Unnecessary pass statements
5. Bad indentation
6. Singleton comparisons
"""

import os
import re
import glob
from pathlib import Path
from typing import List, Tuple

def fix_parser_file(content: str) -> str:
    """Apply all fixes to a parser file."""
    
    # Fix bare except clauses
    content = re.sub(r'except:', 'except Exception:', content)
    
    # Fix file operations with context managers
    # Pattern: file=open(...) ... file.close()
    file_pattern = r'(\w+)\s*=\s*open\(([^)]+)\)\s*\n(.*?)\n\s*\1\.close\(\)'
    
    def convert_to_with(match):
        var_name = match.group(1)
        open_args = match.group(2)
        content_lines = match.group(3)
        
        # Add encoding if not present
        if 'encoding=' not in open_args:
            open_args += ', encoding="utf-8"'
        
        return f'with open({open_args}) as {var_name}:\n{content_lines}'
    
    content = re.sub(file_pattern, convert_to_with, content, flags=re.DOTALL)
    
    # Fix simple open() calls without encoding
    content = re.sub(r'open\(([^)]+)\)', lambda m: f'open({m.group(1)}, encoding="utf-8")' if 'encoding=' not in m.group(1) else m.group(0), content)
    
    # Remove unnecessary pass statements in except blocks
    content = re.sub(r'except[^:]*:\s*\n\s*pass\s*\n', '', content)
    
    # Fix singleton comparisons
    content = re.sub(r'==\s*None', 'is None', content)
    content = re.sub(r'==\s*True', 'is True', content)
    content = re.sub(r'==\s*False', 'is False', content)
    
    # Fix indentation issues (common in some parsers)
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        if line.strip() and line.startswith(' '):
            # Count leading spaces
            leading_spaces = len(line) - len(line.lstrip())
            # Round to nearest 4-space increment
            new_spaces = (leading_spaces // 4) * 4
            line = ' ' * new_spaces + line.lstrip()
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def process_parser_files():
    """Process all parser files."""
    parser_dir = Path('ransomlook/parsers')
    parser_files = list(parser_dir.glob('*.py'))
    
    print(f"Found {len(parser_files)} parser files")
    
    fixed_count = 0
    for parser_file in parser_files:
        try:
            with open(parser_file, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            fixed_content = fix_parser_file(original_content)
            
            if original_content != fixed_content:
                # Create backup
                backup_file = parser_file.with_suffix('.py.backup')
                with open(backup_file, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                
                # Write fixed content
                with open(parser_file, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                print(f"✓ Fixed: {parser_file.name}")
                fixed_count += 1
            else:
                print(f"- No changes: {parser_file.name}")
                
        except Exception as e:
            print(f"✗ Error processing {parser_file.name}: {e}")
    
    print(f"\nFixed {fixed_count} out of {len(parser_files)} parser files")

if __name__ == "__main__":
    process_parser_files()
