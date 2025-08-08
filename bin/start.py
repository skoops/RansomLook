#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import redis
from ransomlook.default.config import get_socket_path

def main() -> None :
    red = redis.Redis(unix_socket_path=get_socket_path('cache'), db=2)
    redleak = redis.Redis(unix_socket_path=get_socket_path('cache'), db=4)
    redleak.set('leaks', '[]')
    redleak.set('groups', '[]')
    red.set('groups', '[]')
    subprocess.run(['poetry', 'run', 'scrape'], check=True)
    subprocess.run(['poetry', 'run', 'parse'], check=True)

if __name__ == '__main__':
    main()
