import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ["BOT_TOKEN"]
WEB_APP_URL = "https://larpe1.github.io/fisch-clicker/"
API = f"https://api.telegram.org/bot{TOKEN}"

@app.route("/")
def home():
    return "Fisch Clicker Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json or {}
    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "")

    if chat_id and text.split() and text.split()[0] == "/start":
        requests.post(f"{API}/sendMessage", json={
            "chat_id": chat_id,
            "text": "🎣 Добро пожаловать в Fisch Clicker!",
            "reply_markup": {
                "inline_keyboard": [[{
                    "text": "🎮 Играть",
                    "web_app": {"url": WEB_APP_URL}
                }]]
            }
        })

    return {"ok": True}

render_url = os.environ.get("RENDER_EXTERNAL_URL")
if render_url:
    requests.post(
        f"{API}/setWebhook",
        json={"url": f"{render_url}/webhook"},
        timeout=10
        )
