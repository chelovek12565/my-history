import telebot
import datetime
from os import listdir
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InputFile, ReplyKeyboardRemove
from telebot.util import quick_markup
from db.__all_models import *
from db.db_session import *

global_init('main_db.db')
TOKEN = "5651637105:AAEzYzH_E8inrezdxr4coOMzOZYL6WNCydU"
bot = telebot.TeleBot(TOKEN)


# Список faq-вопросов
with open('faq_questions.json', 'rt') as faq_file:
    faq_questions = json.loads(faq_file.read())
    faq_names = list(map(lambda x: x[0], faq_questions))
    faq_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    faq_message_text = "Выберите интересующий вас вопрос:"
    buttons = []
    for name, smile, answer in faq_questions:
        # faq_message_text += smile + ' - ' + name + '\n'
        buttons.append(KeyboardButton(text=name))
    faq_keyboard.add(*buttons)


quizes = []
quiz_file_list = listdir('quizes')
for filename in quiz_file_list:
    with open('quizes\\' + filename, 'rt') as quiz_file:
        quizes.append(json.loads(quiz_file.read()))


# guide_messages =
with open('data/match.json', 'rt') as match_file:
    guide_messages = json.loads(match_file.read())
# for key in guide_messages:
#     for sub_key in guide_messages[key]:
#         with open('data/' + guide_messages[key][sub_key], 'rb') as mp3_file:
#             guide_messages[key][sub_key] = InputFile(mp3_file)


@bot.message_handler(commands=['voice'])
def test_voice(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in guide_messages.keys():
        keyboard.add(KeyboardButton(i))
    bot.send_message(message.chat.id, 'Выберите выставку', reply_markup=keyboard)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.reply_to(message, 'Hello world!')


@bot.message_handler(commands=['faq'])
def faq(message):
    """
    Команда для часто задаваемых вопросов
    """
    global faq_messsage_text, faq_keyboard
    bot.send_message(message.chat.id, faq_message_text, reply_markup=faq_keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if '&' in call.data:
        exhibit_name, stand_n = call.data.split('&')
        with open('data/' + guide_messages[exhibit_name][stand_n], 'rb') as mp3_file:
            bot.send_voice(call.message.chat.id, InputFile(mp3_file), reply_markup=ReplyKeyboardRemove())

    bot.answer_callback_query(call.id)


@bot.message_handler(commands=['test_bd'])
def test_bd(message):
    db_sess = create_session()
    user = User()
    user.user_id = message.from_user.id
    user.reg_time = datetime.datetime.now()
    db_sess.add(user)
    db_sess.commit()
    bot.reply_to(message, 'success')
    print("success")


@bot.message_handler(content_types=['text'])
def text_handler(message):
    if message.text in faq_names:
        bot.send_message(message.chat.id, faq_questions[faq_names.index(message.text)][2])
    elif message.text in guide_messages.keys():
        values = {}
        for i in guide_messages[message.text].keys():
            values[i] = {'callback_data': f'{message.text}&{i}'}
        keyboard = quick_markup(values=values, row_width=2)
        bot.send_message(message.chat.id, 'Выберите цифру', reply_markup=keyboard)


bot.infinity_polling()
