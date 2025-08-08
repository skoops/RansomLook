#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import redis
from typing import Dict, Any
from ransomlook.default.config import get_socket_path
import time

def main() -> None :
    red = redis.Redis(unix_socket_path=get_socket_path('cache'), db=3)
    
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd', timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Store cryptocurrency data
        crypto_data = {
            'bitcoin': data.get('bitcoin', {}).get('usd', 0),
            'ethereum': data.get('ethereum', {}).get('usd', 0),
            'timestamp': time.time()
        }
        
        red.set('cryptocurrency', json.dumps(crypto_data))
        print("Updated cryptocurrency data")
        
    except requests.RequestException as e:
        print(f"Failed to fetch cryptocurrency data: {e}")

if __name__ == '__main__':
    main()

