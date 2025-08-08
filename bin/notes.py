#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import redis
from typing import Dict, Any, List
from ransomlook.default.config import get_socket_path

def main() -> None :
    red = redis.Redis(unix_socket_path=get_socket_path('cache'), db=5)
    
    try:
        with open('ransomnotes.json', 'r', encoding='utf-8') as f:
            notes_data = json.load(f)
        
        # Store ransom notes data
        for note in notes_data:
            note_id = note.get('id', 'unknown')
            red.set(f'note_{note_id}', json.dumps(note))
        
        print(f"Loaded {len(notes_data)} ransom notes")
        
    except FileNotFoundError:
        print("ransomnotes.json not found")
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in ransomnotes.json: {e}")
    except Exception as e:
        print(f"Error processing ransom notes: {e}")

if __name__ == '__main__':
    main()
