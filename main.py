import logging
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler


logging.basicConfig(

    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG

)



logger = logging.getLogger(__name__)



TOKEN = 'BOT_TOKEN'


def start(update, context):

    update.message.reply_text(
        "Hello world!")


def echo(update, context):
    update.message.reply_text(update.message.text)





def main():

    updater = Updater(TOKEN)

    dp = updater.dispatcher

    text_handler = MessageHandler(Filters.text, echo)

    dp.add_handler(text_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':

    main()
