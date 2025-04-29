import telebot
from datetime import datetime

TOKEN = "7773544836:AAGyWpzDJWnbxbtgqJhAHfesd6F9NrVuSHo"
bot = telebot.TeleBot(TOKEN)

# /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! ")

# /time
@bot.message_handler(commands=['time'])
def send_time(message):
    current_time = datetime.now().strftime("%H:%M:%S")  # Формат: часы:минуты:секунды
    bot.reply_to(message, f"Время: {current_time}")

# /date
@bot.message_handler(commands=['date'])
def send_date(message):
    current_date = datetime.now().strftime("%d.%m.%Y")  # Формат: день.месяц.год
    bot.reply_to(message, f"Дата: {current_date}")

# эхо
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Я получил сообщение: {message.text}")

# Запуск бота
if __name__ == '__main__':
    print("started")
    bot.polling()