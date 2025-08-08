#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import redis
from typing import Dict, Any, Optional
from ransomlook.default.config import get_config, get_socket_path

def main() -> None :
    red = redis.Redis(unix_socket_path=get_socket_path('cache'), db=2)
    rocketconfig = get_config('generic', 'rocketchat')
    if not rocketconfig['enable']:
        return
    
    groups = red.keys()
    for group in groups:
        posts = json.loads(red.get(group)) # type: ignore
        for post in posts:
            if post.get('discovered'):
                # Check if this is a new post (within last 24 hours)
                import datetime
                post_date = datetime.datetime.strptime(post['discovered'], '%Y-%m-%d %H:%M:%S')
                if (datetime.datetime.now() - post_date).days < 1:
                    message = f"New post from {group.decode()}: {post['post_title']}"
                    if post.get('description'):
                        message += f"\n{post['description']}"
                    
                    # Send to RocketChat
                    try:
                        response = requests.post(
                            rocketconfig['webhook_url'],
                            json={'text': message},
                            timeout=30
                        )
                        response.raise_for_status()
                    except requests.RequestException as e:
                        print(f"Failed to send to RocketChat: {e}")

if __name__ == '__main__':
    main()
