import os
import requests
from bs4 import BeautifulSoup
import telebot
from flask import Flask, request

TOKEN = "8254627470:AAHE-as4aooipypQuT4etiWg1Nel6QFDvn0"


bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)


def get_rate():
    url = 'https://www.tgju.org/profile/geram18'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = "نرخ پیدا نشد!"
    for h3 in soup.find_all('h3'):
        if "نرخ فعلی" in h3.text:
            text = h3.get_text()
            break
    return text


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام 👋 من ربات بررسی نرخ هستم. دستور /price رو بزن تا نرخ فعلی رو بیارم.")


@bot.message_handler(commands=['price'])
def send_price(message):
    rate = get_rate()
    bot.reply_to(message, f"📊 {rate}")


@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200


@app.route("/")
def index():
    return "Bot is running", 200


if __name__ == "__main__":
    WEBHOOK_URL = f"https://telegram-bot-kz6u.onrender.com/{TOKEN}"
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
