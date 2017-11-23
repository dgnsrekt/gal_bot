from logger import getLogger
from gettoken import GetToken

import telegram
from telegram.ext import Updater, CommandHandler

_logger = getLogger()


buttons = [telegram.KeyboardButton('/settings'),
           telegram.KeyboardButton('/gainers'),
           telegram.KeyboardButton('/losers')]

buttons2 = [telegram.KeyboardButton('/(A)'),
            telegram.KeyboardButton('/(B)'),
            telegram.KeyboardButton('/(C)'),
            telegram.KeyboardButton('/(D)'),
            telegram.KeyboardButton('/(E)'),
            telegram.KeyboardButton('/(N)')]


def start(bot, update):
    replymarkup = telegram.ReplyKeyboardMarkup(
        [buttons], resize_keyboard=True, one_time_keyboard=True)
    message = 'Welcom test message.'

    bot.sendMessage(update.message.chat_id, text=message,
                    reply_markup=replymarkup)


def settings(bot, update):
    replymarkup = telegram.ReplyKeyboardMarkup(
        [buttons2], resize_keyboard=True, one_time_keyboard=True)

    message = 'Change Minimum Volume Filter\nA:$25,000\nB:$100,000\nC:$250,000\nD:$500,000\nE:$1,000,000'

    bot.sendMessage(update.message.chat_id, text=message,
                    reply_markup=replymarkup)


def A(bot, update):
    _logger.info('chat_id: {}, user: {}, Changed Filter Settings to A'.format(
        update.message.chat_id, bot.get_chat(update.message.chat_id)['username']))
    message = 'All coins will be filter by a minimum of $25,000.'
    bot.sendMessage(update.message.chat_id, text=message)

updater = Updater(GetToken())

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('settings', settings))
updater.dispatcher.add_handler(CommandHandler('(A)', A))
# updater.dispatcher.add_handler(CommandHandler('(B)'), print('Filter B'))
# updater.dispatcher.add_handler(CommandHandler('(C)'), print('Filter C'))
# updater.dispatcher.add_handler(CommandHandler('(D)'), print('Filter D'))
# updater.dispatcher.add_handler(CommandHandler('(E)'), print('Filter E'))

updater.start_polling()
updater.idle()
