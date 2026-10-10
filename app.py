import csv
import io
import os
from flask import Flask, request, render_template_string, send_file

app = Flask(__name__)
PASSWORD = os.environ.get("DASHBOARD_PASSWORD", "")

PAGE = """
<!doctype html>
<html lang="en">
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Telegram Member List Formatter</title>
<style>
body{font-family:Arial,sans-serif;max-width:680px;margin:28px auto;padding:16px;color:#172033}
.card{border:1px solid #ddd;border-radius:12px;padding:18px}
input,button{width:100%;box-sizing:border-box;padding:12px;margin:8px 0}
button{background:#2563eb;color:white;border:0;border-radius:8px;font-weight:bold}
.note{background:#f4f6f8;padding:12px;border-radius:8px;font-size:14px}
</style>
</head><body>
<h2>Telegram Member List Formatter</h2>
<div class="card">
<p>Upload a CSV you are authorized to use. The tool extracts usernames and prepares a clean CSV.</p>
<form method="post" action="/format" enctype="multipart/form-data">
<input type="file" name="file" accept=".csv,text/csv" required>
<button type="submit">Format & Download CSV</button>
</form>
<div class="note">This tool does not scrape Telegram channels or bypass access restrictions. Telegram does not provide a complete member list for every public channel.</div>
</div></body></html>
"""

@app.get("/")
def home():
    return render_template_string(PAGE)

@app.post("/format")
def format_csv():
    uploaded = request.files.get("file")
    if not uploaded or not uploaded.filename.lower().endswith(".csv"):
        return "Please upload a CSV file.", 400
    try:
        raw = uploaded.stream.read().decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(raw))
        if not reader.fieldnames:
            return "CSV has no header row.", 400
        fields = {name.strip().lower(): name for name in reader.fieldnames if name}
        username_field = next((fields[k] for k in ("username", "user_name", "user name", "handle") if k in fields), None)
        if not username_field:
            return "Could not find a username column. Expected a column named username.", 400
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["username"])
        seen = set()
        for row in reader:
            username = (row.get(username_field) or "").strip().lstrip("@")
            if username and username.lower() not in seen:
                seen.add(username.lower())
                writer.writerow(["@" + username])
        data = io.BytesIO(output.getvalue().encode("utf-8-sig"))
        return send_file(data, mimetype="text/csv", as_attachment=True, download_name="telegram_usernames.csv")
    except UnicodeDecodeError:
        return "CSV must be UTF-8 encoded.", 400
    except Exception:
        return "Could not process this CSV. Check its format and try again.", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
