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

    message = 'Change Minimum Volume Filter\nA:$25,000\nB:$100,000\nC:$250,000\nD:$500,000\nE:$1,000,000\nN:NoFilter'

    bot.sendMessage(update.message.chat_id, text=message,
                    reply_markup=replymarkup)


def changeFilterA(bot, update):
    message_str = 'chat_id: {}, user: {}, Changed Filter Settings to A'

    _logger.info(message_str.format(update.message.chat_id,
                                    bot.get_chat(update.message.chat_id)['username']))

    message = 'All coins will be filter by a minimum of $25,000.'
    bot.sendMessage(update.message.chat_id, text=message)


def changeFilterB(bot, update):
    message_str = 'chat_id: {}, user: {}, Changed Filter Settings to B'

    _logger.info(message_str.format(update.message.chat_id,
                                    bot.get_chat(update.message.chat_id)['username']))

    message = 'All coins will be filter by a minimum of $100,000.'
    bot.sendMessage(update.message.chat_id, text=message)


def changeFilterC(bot, update):
    message_str = 'chat_id: {}, user: {}, Changed Filter Settings to C'

    _logger.info(message_str.format(update.message.chat_id,
                                    bot.get_chat(update.message.chat_id)['username']))

    message = 'All coins will be filter by a minimum of $250,000.'
    bot.sendMessage(update.message.chat_id, text=message)


def changeFilterD(bot, update):
    message_str = 'chat_id: {}, user: {}, Changed Filter Settings to D'

    _logger.info(message_str.format(update.message.chat_id,
                                    bot.get_chat(update.message.chat_id)['username']))

    message = 'All coins will be filter by a minimum of $500,000.'
    bot.sendMessage(update.message.chat_id, text=message)


def changeFilterE(bot, update):
    message_str = 'chat_id: {}, user: {}, Changed Filter Settings to E'

    _logger.info(message_str.format(update.message.chat_id,
                                    bot.get_chat(update.message.chat_id)['username']))

    message = 'All coins will be filter by a minimum of $1,000,000.'
    bot.sendMessage(update.message.chat_id, text=message)


def changeFilterN(bot, update):
    message_str = 'chat_id: {}, user: {}, Changed Filter Settings to N'

    _logger.info(message_str.format(update.message.chat_id,
                                    bot.get_chat(update.message.chat_id)['username']))

    message = 'All coins will be unfiltered'
    bot.sendMessage(update.message.chat_id, text=message)


updater = Updater(GetToken())

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('settings', settings))
updater.dispatcher.add_handler(CommandHandler('(A)', changeFilterA))
updater.dispatcher.add_handler(CommandHandler('(B)', changeFilterB))
updater.dispatcher.add_handler(CommandHandler('(C)', changeFilterC))
updater.dispatcher.add_handler(CommandHandler('(D)', changeFilterD))
updater.dispatcher.add_handler(CommandHandler('(E)', changeFilterE))
updater.dispatcher.add_handler(CommandHandler('(N)', changeFilterN))

updater.start_polling()
updater.idle()
