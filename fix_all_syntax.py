#!/usr/bin/env python3
"""
Fix all remaining syntax errors in parser files

This script comprehensively fixes all syntax errors in the parser files.
"""

import re
import glob
from pathlib import Path

def fix_all_syntax(content: str) -> str:
    """Fix all syntax errors in parser files."""
    
    # Fix duplicate encoding parameters
    content = re.sub(r'encoding="utf-8", encoding="utf-8"', 'encoding="utf-8"', content)
    
    # Fix the specific pattern: with open(...) as file: soup=BeautifulSoup(file,'html.parser')
    pattern = r'with open\(([^)]+)\) as (\w+):\s*(\w+)=BeautifulSoup\(\2,\'html\.parser\'\)'
    
    def fix_context_manager(match):
        open_args = match.group(1)
        var_name = match.group(2)
        soup_var = match.group(3)
        
        return f'''with open({open_args}, encoding="utf-8") as {var_name}:
    {soup_var}=BeautifulSoup({var_name},'html.parser')'''
    
    content = re.sub(pattern, fix_context_manager, content)
    
    # Fix any remaining unindented lines after with statements
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        if line.strip().startswith('with ') and i + 1 < len(lines):
            # Check if next line is not properly indented
            next_line = lines[i + 1]
            if next_line.strip() and not next_line.startswith('    '):
                # Fix indentation
                lines[i + 1] = '    ' + next_line.lstrip()
        fixed_lines.append(line)
    
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
            
            fixed_content = fix_all_syntax(original_content)
            
            if original_content != fixed_content:
                # Create backup
                backup_file = parser_file.with_suffix('.py.backup4')
                with open(backup_file, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                
                # Write fixed content
                with open(parser_file, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                print(f"✓ Fixed all syntax: {parser_file.name}")
                fixed_count += 1
            else:
                print(f"- No syntax fixes needed: {parser_file.name}")
                
        except Exception as e:
            print(f"✗ Error processing {parser_file.name}: {e}")
    
    print(f"\nFixed all syntax in {fixed_count} out of {len(parser_files)} parser files")

if __name__ == "__main__":
    process_parser_files()
