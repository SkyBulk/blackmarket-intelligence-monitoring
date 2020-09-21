# -*- coding: utf-8 -*-

from telethon import TelegramClient, sync
import socks

# Telegram config
api_id = 1244091  # Your api_id
api_hash = "4018f9a21ed122f7bbe0b1413e7c4aae"  # Your api_hash
session_name = 'session_name'
proxy_param = (socks.SOCKS5, 'localhost', 1086)   # Proxy settings, if you need

# Create connection
client = TelegramClient(session_name, api_id, api_hash,
                            proxy=proxy_param).start()
