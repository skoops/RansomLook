#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import redis
from ransomlook.default.config import get_socket_path

def main() -> None :
    try:
        with open('/tmp/ransomlook.pid', 'r', encoding='utf-8') as f:
            pid = f.read().strip()
        subprocess.run(['kill', pid], check=True)
        print(f"Stopped process {pid}")
    except FileNotFoundError:
        print("No PID file found")
    except subprocess.CalledProcessError:
        print("Failed to stop process")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
