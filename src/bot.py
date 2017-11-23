from telegram.ext import Updater, CommandHandler
from gettoken import GetToken
import telegram


def start(bot, update):
    message = 'test message'
    update.message.reply_text(message)


def filter_(bot, update):
    update.message.reply_text(
        'filtered by {}'.format(update.message.from_user.first_name))

updater = Updater(GetToken())

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('filter', filter_))

updater.start_polling()
updater.idle()
