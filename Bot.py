import requests
from bs4 import BeautifulSoup
import telebot

TOKEN = "8254627470:AAHE-as4aooipypQuT4etiWg1Nel6QFDvn0"
bot = telebot.TeleBot(TOKEN)

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

print("✅ ربات روشن شد...")
bot.infinity_polling()
