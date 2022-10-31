import telebot
import datetime
import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.__all_models import *
from db.db_session import *

global_init('main_db.db')
TOKEN = "5651637105:AAEzYzH_E8inrezdxr4coOMzOZYL6WNCydU"
bot = telebot.TeleBot(TOKEN)


with open('questions.json', 'rt') as  faq_file:
    faq_questions = json.loads(faq_file.read())
    faq_smiles = list(map(lambda x: x[1], faq_questions))
    faq_keyboard = InlineKeyboardMarkup()
    faq_message_text = ""
    buttons = []
    for name, smile, answer in faq_questions:
        faq_message_text += smile + ' - ' + name + '\n'
        buttons.append(InlineKeyboardButton(text=smile, callback_data=smile, row_width=2))
    faq_keyboard.add(*buttons, row_width=2)
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
def callback_hanler(call):
    global faq_smiles, faq_keyboard, faq_questions
    if call.data in faq_smiles:
        bot.send_message(call.message.chat.id, faq_questions[faq_smiles.index(call.data)][2],
                         reply_markup=faq_keyboard)
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



bot.infinity_polling()