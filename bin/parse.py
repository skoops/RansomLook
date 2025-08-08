#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import importlib.util
import json
import redis
from typing import List, Dict, Any

from ransomlook.default.config import get_socket_path

def main() -> None :
    red = redis.Redis(unix_socket_path=get_socket_path('cache'), db=2)
    redleak = redis.Redis(unix_socket_path=get_socket_path('cache'), db=4)
    groups = red.keys()
    leaks = redleak.keys()
    for group in groups:
        try:
            group_data = json.loads(red.get(group)) # type: ignore
            if group_data:
                group_name = group.decode()
                parser_name = group_name.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('.', '').lower()
                parser_path = f'ransomlook.parsers.{parser_name}'
                try:
                    parser_module = importlib.import_module(parser_path)
                    if hasattr(parser_module, 'main'):
                        parser_result = parser_module.main()
                        if parser_result:
                            red.set(group, json.dumps(parser_result))
                            print(f"Updated {group_name}")
                except ImportError:
                    print(f"No parser found for {group_name}")
        except Exception as e:
            print(f"Error processing {group}: {e}")

    for leak in leaks:
        try:
            leak_data = json.loads(redleak.get(leak)) # type: ignore
            if leak_data:
                leak_name = leak.decode()
                parser_name = leak_name.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('.', '').lower()
                parser_path = f'ransomlook.parsers.{parser_name}'
                try:
                    parser_module = importlib.import_module(parser_path)
                    if hasattr(parser_module, 'main'):
                        parser_result = parser_module.main()
                        if parser_result:
                            redleak.set(leak, json.dumps(parser_result))
                            print(f"Updated {leak_name}")
                except ImportError:
                    print(f"No parser found for {leak_name}")
        except Exception as e:
            print(f"Error processing {leak}: {e}")

if __name__ == '__main__':
    main()

