# Telegram Channel Member Exporter

Public Telegram channel ke members CSV mein export karta hai.

## Setup
1. https://my.telegram.org se api_id aur api_hash lein
2. Local machine / Termux par `auth_session.py` chala kar session string banayein
3. GitHub par upload karein
4. Render par deploy karein
5. Env vars set karein: TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_SESSION, SECRET_KEY

## Limitation
- Sirf public channels
- Max ~200 members (Telegram ki limit)
