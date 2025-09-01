import os
import requests
from bs4 import BeautifulSoup
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from flask import Flask, request

TOKEN = '8254627470:AAHE-as4aooipypQuT4etiWg1Nel6QFDvn0'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)


# --- تابع دریافت نرخ ---
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


# --- کیبورد اصلی ---
def main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        KeyboardButton("/price"),
        KeyboardButton("/help")
    )
    return keyboard


# --- دستور start ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "سلام 👋\nمن ربات بررسی نرخ طلا هستم. از دکمه‌ها استفاده کن یا دستور /price رو بزن.",
        reply_markup=main_keyboard()
    )


# --- دستور help ---
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(
        message.chat.id,
        "دستورات ربات:\n"
        "/price - نمایش نرخ فعلی طلا\n"
        "/help - نمایش این پیام"
    )


# --- دستور price ---
@bot.message_handler(commands=['price'])
def send_price(message):
    rate = get_rate()
    bot.send_message(message.chat.id, f"📊 نرخ فعلی: {rate}")


# --- Webhook endpoint ---
@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200


@app.route("/")
def index():
    return "Bot is running", 200


# --- اجرای وب‌سرور ---
if __name__ == "__main__":
    WEBHOOK_URL = f"https://telegram-bot-kz6u.onrender.com/{TOKEN}"
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
