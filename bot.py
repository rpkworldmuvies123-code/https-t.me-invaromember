import os
import csv
import io
import asyncio
from flask import Flask, request, render_template, send_file
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret")

API_ID = int(os.environ.get("TELEGRAM_API_ID", "0"))
API_HASH = os.environ.get("TELEGRAM_API_HASH", "")
SESSION_STRING = os.environ.get("TELEGRAM_SESSION", "")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        channel_username = request.form.get("channel", "").strip().replace("@", "")
        if not channel_username:
            return render_template("index.html", error="Channel username daalein")

        try:
            members = asyncio.run(fetch_members(channel_username))
            if not members:
                return render_template(
                    "index.html",
                    error="Koi member nahi mila. Channel public hai? Username sahi hai?"
                )

            csv_data = generate_csv(members)
            return send_file(
                io.BytesIO(csv_data.encode("utf-8")),
                mimetype="text/csv",
                as_attachment=True,
                download_name=f"{channel_username}_members.csv",
            )
        except Exception as e:
            return render_template("index.html", error=f"Error: {str(e)}")

    return render_template("index.html")


async def fetch_members(channel_username):
    if not SESSION_STRING:
        raise Exception("TELEGRAM_SESSION env variable set nahi hai")

    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        await client.disconnect()
        raise Exception("Session invalid hai. Dobara auth karein.")

    try:
        entity = await client.get_entity(channel_username)

        members = []
        offset = 0
        limit = 200

        while True:
            result = await client(GetParticipantsRequest(
                channel=entity,
                filter=ChannelParticipantsSearch(''),
                offset=offset,
                limit=limit,
                hash=0
            ))
            if not result.users:
                break

            for user in result.users:
                members.append({
                    "id": user.id,
                    "username": user.username or "",
                    "first_name": user.first_name or "",
                    "last_name": user.last_name or "",
                    "phone": user.phone or "Hidden",
                    "bot": "Yes" if user.bot else "No",
                    "verified": "Yes" if user.verified else "No",
                })

            offset += len(result.users)
            if len(result.users) < limit:
                break
            if offset >= 200:
                break

        return members
    finally:
        await client.disconnect()


def generate_csv(members):
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=["id", "username", "first_name", "last_name", "phone", "bot", "verified"],
    )
    writer.writeheader()
    for m in members:
        writer.writerow(m)
    return output.getvalue()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
