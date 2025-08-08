#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys
import redis
import time
from typing import Dict, Any
from ransomlook.default.config import get_socket_path

def main() -> None :
    try:
        # Start Valkey server
        subprocess.run(['valkey-server', '--daemonize', 'yes'], check=True)
        print("Started Valkey server")
        
        # Wait for server to be ready
        time.sleep(2)
        
        # Test connection
        red = redis.Redis(unix_socket_path=get_socket_path('cache'), db=0)
        red.ping()
        print("Valkey connection successful")
        
        # Initialize databases
        for db_num in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]:
            db = redis.Redis(unix_socket_path=get_socket_path('cache'), db=db_num)
            db.ping()
            print(f"Database {db_num} initialized")
            
    except subprocess.CalledProcessError as e:
        print(f"Failed to start Valkey: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
