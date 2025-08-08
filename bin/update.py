#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys
import os
from typing import List, Dict, Any

def main() -> None :
    """Update RansomLook components."""
    
    # Update dependencies
    try:
        subprocess.run(['poetry', 'install'], check=True)
        print("Dependencies updated")
    except subprocess.CalledProcessError as e:
        print(f"Failed to update dependencies: {e}")
        return
    
    # Update web assets
    try:
        subprocess.run(['poetry', 'run', 'tools/3rdparty.py'], check=True)
        print("Web assets updated")
    except subprocess.CalledProcessError as e:
        print(f"Failed to update web assets: {e}")
    
    # Generate SRI hashes
    try:
        subprocess.run(['poetry', 'run', 'tools/generate_sri.py'], check=True)
        print("SRI hashes generated")
    except subprocess.CalledProcessError as e:
        print(f"Failed to generate SRI hashes: {e}")
    
    print("Update completed")

if __name__ == '__main__':
    main()
