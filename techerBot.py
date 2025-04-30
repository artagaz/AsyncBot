import json
import random
import telebot
from telebot import types

TOKEN = '7678405561:AAEz49yrvJH7YcZJAxMs8G544ClmEjumNFA'
QUESTIONS_FILE = 'questions.json'
bot = telebot.TeleBot(TOKEN)

user_data = {}


class UserData:
    def __init__(self):
        self.questions = []
        self.current_question = 0
        self.correct_answers = 0
        self.test_active = False


def load_questions():
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        questions = data['test']
        random.shuffle(questions)
        return questions[:10]


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_data[chat_id] = UserData()
    user_data[chat_id].questions = load_questions()
    user_data[chat_id].current_question = 0
    user_data[chat_id].correct_answers = 0
    user_data[chat_id].test_active = True

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('Да', 'Нет')

    bot.send_message(chat_id,
                     f"Привет! Я задам тебе {len(user_data[chat_id].questions)} вопросов. Готов начать?",
                     reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in ['Да', 'Нет'] and
                                          message.chat.id in user_data and
                                          user_data[message.chat.id].test_active and
                                          user_data[message.chat.id].current_question == 0)
def handle_start_response(message):
    chat_id = message.chat.id
    if message.text == 'Нет':
        bot.send_message(chat_id,
                         "начать заново: /start",
                         reply_markup=types.ReplyKeyboardRemove())
        user_data[chat_id].test_active = False
    else:
        ask_question(chat_id)


def ask_question(chat_id):
    user = user_data[chat_id]
    if user.current_question < len(user.questions):
        question = user.questions[user.current_question]['question']
        bot.send_message(chat_id,
                         f"Вопрос {user.current_question + 1}/{len(user.questions)}:\n{question}",
                         reply_markup=types.ReplyKeyboardRemove())
        user.current_question += 1
    else:
        finish_test(chat_id)


@bot.message_handler(func=lambda message: message.chat.id in user_data and
                                          user_data[message.chat.id].test_active and
                                          user_data[message.chat.id].current_question > 0 and
                                          user_data[message.chat.id].current_question <= len(user_data[message.chat.id].questions))
def handle_answer(message):
    chat_id = message.chat.id
    user = user_data[chat_id]

    question_index = user.current_question - 1
    user_answer = message.text
    correct_answer = user.questions[question_index]['response']

    if user_answer.lower() == '/stop':
        stop(message)

    if user_answer.lower() == correct_answer.lower():
        user.correct_answers += 1
        bot.send_message(chat_id, "Правильно")
    else:
        bot.send_message(chat_id, f"Неправильно. Правильный ответ: {correct_answer}")

    ask_question(chat_id)


def finish_test(chat_id):
    user = user_data[chat_id]
    result = f"Тест завершен.\nПравильных ответов: {user.correct_answers}/{len(user.questions)}"

    bot.send_message(chat_id,
                     result + "\n\nЕще раз: /start",
                     reply_markup=types.ReplyKeyboardRemove())
    user.test_active = False


@bot.message_handler(commands=['stop'])
def stop(message):
    chat_id = message.chat.id
    if chat_id in user_data:
        user_data[chat_id].test_active = False
    bot.send_message(chat_id,
                     "начать заново: /start",
                     reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    chat_id = message.chat.id
    if chat_id not in user_data or not user_data[chat_id].test_active:
        bot.send_message(chat_id, "Напиши /start чтобы начать тест или /stop чтобы прервать")


if __name__ == '__main__':
    print("started")
    bot.infinity_polling()
