import os
from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID = int(os.environ.get("TELEGRAM_API_ID", "0"))
API_HASH = os.environ.get("TELEGRAM_API_HASH", "")

with TelegramClient(StringSession(), API_ID, API_HASH) as client:
    print("\n=== SESSION STRING (copy karein) ===")
    print(client.session.save())
    print("=====================================\n")
