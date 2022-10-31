import telebot
import datetime
from db.__all_models import *
from db.db_session import *

global_init('main_db.db')
TOKEN = "5651637105:AAEzYzH_E8inrezdxr4coOMzOZYL6WNCydU"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message):
   bot.reply_to(message, 'Hello world!')


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