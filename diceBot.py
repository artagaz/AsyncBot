import telebot
from telebot import types
import random
import threading

TOKEN = "7756681527:AAFRzvPURtvjww6NPAwi6AoLzDZVOiMNRJs"
bot = telebot.TeleBot(TOKEN)

# Словарь для хранения активных таймеров
active_timers = {}


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_dice = types.KeyboardButton('/dice')
    btn_timer = types.KeyboardButton('/timer')
    markup.add(btn_dice, btn_timer)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)


# Обработчик команды /dice
@bot.message_handler(commands=['dice'])
def dice_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_d6 = types.KeyboardButton('кинуть один шестигранный кубик')
    btn_2d6 = types.KeyboardButton('кинуть 2 шестигранных кубика одновременно')
    btn_d20 = types.KeyboardButton('кинуть 20-гранный кубик')
    btn_back = types.KeyboardButton('вернуться назад')
    markup.add(btn_d6, btn_2d6, btn_d20, btn_back)
    bot.send_message(message.chat.id, "Выберите кубик:", reply_markup=markup)


# Обработчик команды /timer
@bot.message_handler(commands=['timer'])
def timer_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_30s = types.KeyboardButton('30 секунд')
    btn_1m = types.KeyboardButton('1 минута')
    btn_5m = types.KeyboardButton('5 минут')
    btn_back = types.KeyboardButton('вернуться назад')
    markup.add(btn_30s, btn_1m, btn_5m, btn_back)
    bot.send_message(message.chat.id, "Выберите таймер:", reply_markup=markup)


# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    chat_id = message.chat.id

    # Обработка кубиков
    if message.text == 'кинуть один шестигранный кубик':
        result = random.randint(1, 6)
        bot.send_message(chat_id, f"Выпало: {result}")
    elif message.text == 'кинуть 2 шестигранных кубика одновременно':
        result1 = random.randint(1, 6)
        result2 = random.randint(1, 6)
        bot.send_message(chat_id, f"Выпало: {result1} и {result2}")
    elif message.text == 'кинуть 20-гранный кубик':
        result = random.randint(1, 20)
        bot.send_message(chat_id, f"Выпало: {result}")

    # Обработка таймеров
    elif message.text == '30 секунд':
        start_timer(chat_id, 30, "30 секунд")
    elif message.text == '1 минута':
        start_timer(chat_id, 60, "1 минута")
    elif message.text == '5 минут':
        start_timer(chat_id, 300, "5 минут")

    # Обработка кнопки Назад
    elif message.text == 'вернуться назад':
        send_welcome(message)

    # Обработка кнопки Закрыть
    elif message.text == '/close':
        if chat_id in active_timers:
            active_timers[chat_id].cancel()
            del active_timers[chat_id]
            bot.send_message(chat_id, "Таймер отменён")
        else:
            bot.send_message(chat_id, "Нет активных таймеров")


# Функция запуска таймера
def start_timer(chat_id, seconds, timer_name):
    bot.send_message(chat_id, f"засек {timer_name}")

    # Создаем клавиатуру с кнопкой /close
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_close = types.KeyboardButton('/close')
    markup.add(btn_close)
    btn_back = types.KeyboardButton('вернуться назад')
    markup.add(btn_back)
    bot.send_message(chat_id, "Таймер запущен", reply_markup=markup)

    # Создаем и запускаем таймер
    timer = threading.Timer(seconds, timer_completed, args=[chat_id, timer_name])
    active_timers[chat_id] = timer
    timer.start()


# Функция, вызываемая по завершении таймера
def timer_completed(chat_id, timer_name):
    if chat_id in active_timers:
        del active_timers[chat_id]
    bot.send_message(chat_id, f"{timer_name} истекло")
    send_welcome(chat_id)  # Возвращаем стартовое меню


if __name__ == '__main__':
    print("started")
    bot.polling()