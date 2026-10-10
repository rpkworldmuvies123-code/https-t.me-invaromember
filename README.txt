TELEGRAM MEMBER LIST FORMATTER — RENDER SETUP

This project formats a CSV file you are authorized to use. It does not scrape arbitrary public Telegram channels. Telegram does not expose complete member lists for every public channel.

SETUP FROM MOBILE:
1. Download and extract this ZIP.
2. Create a GitHub repository and upload app.py, requirements.txt, and render.yaml.
3. Open https://render.com and sign in.
4. Choose New + > Web Service, then connect the GitHub repository.
5. Render should detect render.yaml. If asked, use:
   Build command: pip install -r requirements.txt
   Start command: gunicorn app:app
6. Deploy, then open the Render URL.
7. Upload a CSV containing a column named "username" and tap Format & Download CSV.

The app only processes the CSV you upload; it does not connect to Telegram or request your Telegram login code.
