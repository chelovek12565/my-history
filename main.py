import telebot
import datetime
from os import listdir
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
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


# @bot.callback_query_handler(func=lambda call: True)
# def callback_hanler(call):
#     global faq_smiles, faq_keyboard, faq_questions
#     if call.data in faq_smiles:
#         bot.send_message(call.message.chat.id, faq_questions[faq_smiles.index(call.data)][2],
#                          reply_markup=faq_keyboard)
#     bot.answer_callback_query(call.id)


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


bot.infinity_polling()
