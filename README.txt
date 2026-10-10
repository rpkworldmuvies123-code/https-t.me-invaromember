TELEGRAM BOT — MOBILE + RENDER SETUP

FILES TO UPLOAD TO THE ROOT OF YOUR GITHUB REPOSITORY:
1. bot.py
2. requirements.txt
3. render.yaml

RENDER:
1. Render > New + > Background Worker (or create from render.yaml) > connect GitHub repository.
2. Build command: pip install -r requirements.txt
3. Start command: python bot.py
4. Environment variable:
   Key: BOT_TOKEN
   Value: token from @BotFather
5. Deploy. Open your bot in Telegram and send /start.

IMPORTANT:
- This is a Telegram bot, not a website.
- It checks basic public channel information and attempts to show member count.
- Telegram Bot API does not provide a complete member list for arbitrary public channels; this bot does not scrape/export all members.
- Never upload BOT_TOKEN to GitHub or share it publicly.
- Render background workers may require a paid plan depending on current Render offerings.
