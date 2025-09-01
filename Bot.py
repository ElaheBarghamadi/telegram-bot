import os
import requests
from bs4 import BeautifulSoup
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from flask import Flask, request

TOKEN = '8254627470:AAHE-as4aooipypQuT4etiWg1Nel6QFDvn0'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)


# --- تابع استخراج اطلاعات داینامیک از سایت ---
def get_rate_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    data = {}

    # پیدا کردن جدول‌ها
    table = soup.find("table")
    if table:
        for row in table.find_all("tr"):
            cols = row.find_all("td")
            if len(cols) >= 2:
                key = cols[0].text.strip()
                value = cols[1].text.strip()
                data[key] = value

    # اگر چیزی پیدا نشد، پیام خطا
    if not data:
        return "❌ اطلاعات پیدا نشد!"

    # مرتب کردن خروجی
    text = ""
    for key in ["نرخ فعلی", "بالاترین قیمت روز", "پایین ترین قیمت روز",
                "نرخ روز گذشته", "درصد تغییر نسبت به روز گذشته"]:
        if key in data:
            text += f"{key}: {data[key]}\n"
    return text


URLS = {
    "gold": "https://www.tgju.org/profile/geram18",
    "dollar": "https://www.tgju.org/profile/price_dollar",
    "tether": "https://www.tgju.org/profile/price_tether"
}


# --- کیبورد اصلی ---
def main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        KeyboardButton("/gold"),
        KeyboardButton("/dollar"),
        KeyboardButton("/tether"),
        KeyboardButton("/help")
    )
    return keyboard


# --- دستورات ربات ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "سلام 👋\nمن ربات بررسی نرخ ارز و طلا هستم. از دکمه‌ها استفاده کن یا دستور مورد نظر را بزن.",
        reply_markup=main_keyboard()
    )


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(
        message.chat.id,
        "دستورات ربات:\n"
        "/gold - نمایش نرخ طلا\n"
        "/dollar - نمایش نرخ دلار\n"
        "/tether - نمایش نرخ تتر\n"
        "/help - نمایش این پیام"
    )


@bot.message_handler(commands=['gold', 'dollar', 'tether'])
def send_rate(message):
    cmd = message.text.replace("/", "")
    if cmd in URLS:
        text = get_rate_details(URLS[cmd])
        emojis = {"gold": "📊", "dollar": "💵", "tether": "🪙"}
        bot.send_message(message.chat.id, f"{emojis.get(cmd, '')} نرخ {cmd}:\n{text}")
    else:
        bot.send_message(message.chat.id, "❌ دستور نامعتبر است!")


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
    WEBHOOK_URL = f"https://آدرس_ربات_تو/{TOKEN}"
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
