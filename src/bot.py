from logger import getLogger
from gettoken import GetToken

import telegram
from telegram.ext import Updater, CommandHandler

from model import UserSettings, createTables

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


def getUserID(update):
    return update.message.chat_id


def getUserName(bot, update):
    return bot.get_chat(getUserID(update))['username']


def addUserToDatabase(bot, update):
    UserSettings.addUser(chat_id=getUserID(update), filter_settings='N')


def updateUserDatbase(bot, update, setting):
    UserSettings.updateUserSettings(
        chat_id=getUserID(update), filter_settings=setting)


def start(bot, update):
    replymarkup = telegram.ReplyKeyboardMarkup(
        [buttons], resize_keyboard=True, one_time_keyboard=True)

    message = 'Welcome to the CMC Gainers and Losers bot.\n'
    message += '/start - reset settings\n' + '/menu\t-\tMain Menu\n'
    message += '/settings\t-\tFilter Settings\n' + '/gainers\t-\t1h, 24h, 7D\n'
    message += '/losers\t-\t1h, 24h, 7D\n'
    addUserToDatabase(bot, update)

    bot.sendMessage(getUserID(update), text=message,
                    reply_markup=replymarkup)


def settings(bot, update):
    replymarkup = telegram.ReplyKeyboardMarkup(
        [buttons2], resize_keyboard=True, one_time_keyboard=True)

    message = 'Change Minimum Volume Filter\nA:$25,000\nB:$100,000\nC:$250,000\nD:$500,000\nE:$1,000,000\nN:NoFilter'

    bot.sendMessage(getUserID(update), text=message,
                    reply_markup=replymarkup)


def menu(bot, update):
    replymarkup = telegram.ReplyKeyboardMarkup(
        [buttons], resize_keyboard=True, one_time_keyboard=True)

    message = '/menu\t-\tMain Menu\n'
    message += '/settings\t-\tFilter Settings\n' + '/gainers\t-\t1h, 24h, 7D\n'
    message += '/losers\t-\t1h, 24h, 7D\n'

    bot.sendMessage(getUserID(update), text=message,
                    reply_markup=replymarkup)


def baseFilter(bot, update, log_str, message, filter_setting):
    updateUserDatbase(bot, update, filter_setting)
    _logger.info(log_str.format(
        getUserID(update), getUserName(bot, update)))

    replymarkup = telegram.ReplyKeyboardMarkup(
        [buttons], resize_keyboard=True, one_time_keyboard=True)

    bot.sendMessage(getUserID(update), text=message, reply_markup=replymarkup)


def changeFilterA(bot, update):
    log_str = 'chat_id: {}, user: {}, Changed Filter Settings to A'
    message = 'All coins will be filter by a minimum of $25,000.'
    baseFilter(bot, update, log_str, message, 'A')


def changeFilterB(bot, update):
    log_str = 'chat_id: {}, user: {}, Changed Filter Settings to B'
    message = 'All coins will be filter by a minimum of $100,000.'
    baseFilter(bot, update, log_str, message, 'B')


def changeFilterC(bot, update):
    log_str = 'chat_id: {}, user: {}, Changed Filter Settings to C'
    message = 'All coins will be filter by a minimum of $250,000.'
    baseFilter(bot, update, log_str, message, 'C')


def changeFilterD(bot, update):
    log_str = 'chat_id: {}, user: {}, Changed Filter Settings to D'
    message = 'All coins will be filter by a minimum of $500,000.'
    baseFilter(bot, update, log_str, message, 'D')


def changeFilterE(bot, update):
    log_str = 'chat_id: {}, user: {}, Changed Filter Settings to E'
    message = 'All coins will be filter by a minimum of $1,000,000.'
    baseFilter(bot, update, log_str, message, 'E')


def changeFilterN(bot, update):
    log_str = 'chat_id: {}, user: {}, Changed Filter Settings to N'
    message = 'All coins will be unfiltered'
    baseFilter(bot, update, log_str, message, 'N')


updater = Updater(GetToken())

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('settings', settings))
updater.dispatcher.add_handler(CommandHandler('menu', menu))
updater.dispatcher.add_handler(CommandHandler('(A)', changeFilterA))
updater.dispatcher.add_handler(CommandHandler('(B)', changeFilterB))
updater.dispatcher.add_handler(CommandHandler('(C)', changeFilterC))
updater.dispatcher.add_handler(CommandHandler('(D)', changeFilterD))
updater.dispatcher.add_handler(CommandHandler('(E)', changeFilterE))
updater.dispatcher.add_handler(CommandHandler('(N)', changeFilterN))

updater.start_polling()
updater.idle()


# TODO ADD MENU FUNCTION FOR EASE OF USE
# ADD ERROR FUNCTION
