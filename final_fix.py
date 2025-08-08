#!/usr/bin/env python3
"""
Final comprehensive fix for all syntax errors

This script fixes all remaining syntax errors in the parser files.
"""

import re
import glob
from pathlib import Path

def final_fix(content: str) -> str:
    """Final comprehensive fix for all syntax errors."""
    
    # Fix duplicate encoding parameters
    content = re.sub(r'encoding="utf-8", encoding="utf-8"', 'encoding="utf-8"', content)
    
    # Fix the specific pattern with unindented lines after with statements
    lines = content.split('\n')
    fixed_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check if this is a with statement
        if line.strip().startswith('with ') and i + 1 < len(lines):
            fixed_lines.append(line)
            
            # Check the next line
            next_line = lines[i + 1]
            if next_line.strip() and not next_line.startswith('    '):
                # Fix indentation
                fixed_lines.append('    ' + next_line.lstrip())
                i += 1
            else:
                fixed_lines.append(next_line)
                i += 1
        else:
            fixed_lines.append(line)
        
        i += 1
    
    return '\n'.join(fixed_lines)

def process_parser_files():
    """Process all parser files to fix all syntax errors."""
    parser_dir = Path('ransomlook/parsers')
    parser_files = list(parser_dir.glob('*.py'))
    
    print(f"Found {len(parser_files)} parser files to fix")
    
    fixed_count = 0
    for parser_file in parser_files:
        try:
            with open(parser_file, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            fixed_content = final_fix(original_content)
            
            if original_content != fixed_content:
                # Create backup
                backup_file = parser_file.with_suffix('.py.backup5')
                with open(backup_file, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                
                # Write fixed content
                with open(parser_file, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                print(f"✓ Final fix: {parser_file.name}")
                fixed_count += 1
            else:
                print(f"- No final fixes needed: {parser_file.name}")
                
        except Exception as e:
            print(f"✗ Error processing {parser_file.name}: {e}")
    
    print(f"\nFinal fixes applied to {fixed_count} out of {len(parser_files)} parser files")

if __name__ == "__main__":
    process_parser_files()
