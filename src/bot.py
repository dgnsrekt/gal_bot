from logger import getLogger
from gettoken import GetToken
from donate import getDonateLink

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from model import UserSettings, createTables
from scraper import getDataFromPickle

_logger = getLogger()


KEYBOARD_MAIN = [telegram.KeyboardButton('/settings'),
                 telegram.KeyboardButton('/gainers'),
                 telegram.KeyboardButton('/losers'),
                 telegram.KeyboardButton('/donate')]

KEYBOARD_SETTINGS = [telegram.KeyboardButton('/(A)'),
                     telegram.KeyboardButton('/(B)'),
                     telegram.KeyboardButton('/(C)'),
                     telegram.KeyboardButton('/(D)'),
                     telegram.KeyboardButton('/(E)'),
                     telegram.KeyboardButton('/(N)')]

KEYBOARD_DONATE = [telegram.KeyboardButton('/BTC'),
                   telegram.KeyboardButton('/BCH'),
                   telegram.KeyboardButton('/ETH'),
                   telegram.KeyboardButton('/ETC'),
                   telegram.KeyboardButton('/ZEC')]


def getUserID(update):
    return update.message.chat_id


def getUserName(bot, update):
    return bot.get_chat(getUserID(update))['username']


def addUserToDatabase(bot, update):
    UserSettings.addUser(chat_id=getUserID(update), filter_settings='N')


def updateUserDatbase(bot, update, setting):
    UserSettings.updateUserSettings(
        chat_id=getUserID(update), filter_settings=setting)


def getUserSettingFromDatabase(bot, update):
    return UserSettings.getUserSettings(chat_id=getUserID(update))


def returnBasicMessage(bot, update):
    filterSetting = getUserSettingFromDatabase(bot, update)

    message = 'Please use the following commands.\n\n'
    message += '/start       - Initializes bot.\n'
    message += '/menu     - Main Menu\n'
    message += '/settings  - Filter Settings\n'
    message += '/gainers   - Shows 1h, 24h, 7D gainers.\n'
    message += '/losers     - Shows 1h, 24h, 7D losers.\n'
    message += '/donate   - If you love the bot.\n\n'
    message += 'Filter Set to: {}'.format(returnFilterMessage(filterSetting))

    return message


def sendMessageWithKeyboard(bot, update, message, keyboard):
    replymarkup = telegram.ReplyKeyboardMarkup(
        [keyboard], resize_keyboard=True, one_time_keyboard=True)
    bot.sendMessage(getUserID(update), text=message,
                    reply_markup=replymarkup, parse_mode=telegram.ParseMode.HTML)


def start(bot, update):
    message = 'Welcome to the Gainers/Losers bot.\n'
    message += returnBasicMessage(bot, update)

    addUserToDatabase(bot, update)
    sendMessageWithKeyboard(bot, update, message, KEYBOARD_MAIN)


def settings(bot, update):
    message = 'Change Minimum 24hr Volume Filter\n'
    message += 'A: > $25,000\n'
    message += 'B: > $100,000\n'
    message += 'C: > $250,000\n'
    message += 'D: > $500,000\n'
    message += 'E: > $1,000,000\n'
    message += 'N:   NoFilter'

    sendMessageWithKeyboard(bot, update, message, KEYBOARD_SETTINGS)


def menu(bot, update):
    message = returnBasicMessage(bot, update)

    sendMessageWithKeyboard(bot, update, message, KEYBOARD_MAIN)


def baseFilter(bot, update, log_str, message, filter_setting):
    updateUserDatbase(bot, update, filter_setting)
    _logger.info(log_str.format(
        getUserID(update), getUserName(bot, update)))

    sendMessageWithKeyboard(bot, update, message, KEYBOARD_MAIN)


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


def returnFilterMessage(filterSetting):
    message = {'A': '> $25,000',
               'B': '> $10,0000',
               'C': '> $25,0000',
               'D': '> $50,0000',
               'E': '> $1,000,000',
               'N': 'No Filter'}
    return message[filterSetting]


def htmlFixedMessage(message):
    if 'Empty DataFrame' not in message:
        return '<pre>{}</pre>'.format(message.replace('Pct', '%Chg'))
    return '<pre>No Data Avaliable</pre>'


def gainers(bot, update):
    filterSetting = getUserSettingFromDatabase(bot, update)
    gainData = getDataFromPickle(filterSetting)

    message = 'Biggest Gainers Last Hour {}'.format(
        returnFilterMessage(filterSetting)) + '\n\n'
    message += htmlFixedMessage(gainData['gainers_1h']) + '\n\n'

    message += 'Biggest Gainers Last 24 Hours {}'.format(
        returnFilterMessage(filterSetting)) + '\n\n'
    message += htmlFixedMessage(gainData['gainers_24h']) + '\n\n'

    message += 'Biggest Gainers Last 7 Days {}'.format(
        returnFilterMessage(filterSetting)) + '\n\n'
    message += htmlFixedMessage(gainData['gainers_7d']) + '\n\n'

    sendMessageWithKeyboard(bot, update, message, KEYBOARD_MAIN)


def losers(bot, update):
    filterSetting = getUserSettingFromDatabase(bot, update)
    loseData = getDataFromPickle(filterSetting)

    message = 'Biggest Losers Last Hour {}'.format(
        returnFilterMessage(filterSetting)) + '\n\n'
    message += htmlFixedMessage(loseData['losers_1h']) + '\n\n'

    message += 'Biggest Losers Last 24 Hours {}'.format(
        returnFilterMessage(filterSetting)) + '\n\n'
    message += htmlFixedMessage(loseData['losers_24h']) + '\n\n'

    message += 'Biggest Losers Last 7 Days {}'.format(
        returnFilterMessage(filterSetting)) + '\n\n'
    message += htmlFixedMessage(loseData['losers_7d']) + '\n\n'

    sendMessageWithKeyboard(bot, update, message, KEYBOARD_MAIN)


def donate(bot, update):
    message = 'BTC ' + 'BCH ' + 'ETH ' + 'ETC ' + 'ZEC ' + '\n'
    message += 'Donate if you like/use the bot.'

    sendMessageWithKeyboard(bot, update, message, KEYBOARD_DONATE)


def getBTC(bot, update):
    message = getDonateLink('BTC')
    _logger.info('{}:{} maybe donating BTC'.format(
        getUserID(update), getUserName(bot, update)))
    sendMessageWithKeyboard(bot, update, message, KEYBOARD_MAIN)


def getBCH(bot, update):
    message = getDonateLink('BCH')
    _logger.info('{}:{} maybe donating BCH'.format(
        getUserID(update), getUserName(bot, update)))
    sendMessageWithKeyboard(bot, update, message, KEYBOARD_MAIN)


def getETH(bot, update):
    message = getDonateLink('ETH')
    _logger.info('{}:{} maybe donating ETH'.format(
        getUserID(update), getUserName(bot, update)))
    sendMessageWithKeyboard(bot, update, message, KEYBOARD_MAIN)


def getETC(bot, update):
    message = getDonateLink('ETC')
    _logger.info('{}:{} maybe donating ETC'.format(
        getUserID(update), getUserName(bot, update)))
    sendMessageWithKeyboard(bot, update, message, KEYBOARD_MAIN)


def getZEC(bot, update):
    message = getDonateLink('ZEC')
    _logger.info('{}:{} maybe donating ZEC'.format(
        getUserID(update), getUserName(bot, update)))
    sendMessageWithKeyboard(bot, update, message, KEYBOARD_MAIN)


def error(bot, update, error):
    _logger.warning('Update {} caused error {}'.format(update, error))


def main():
    createTables()
    updater = Updater(GetToken())

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('settings', settings))
    updater.dispatcher.add_handler(CommandHandler('menu', menu))
    updater.dispatcher.add_handler(CommandHandler('help', menu))

    updater.dispatcher.add_handler(CommandHandler('donate', donate))

    updater.dispatcher.add_handler(CommandHandler('BTC', getBTC))
    updater.dispatcher.add_handler(CommandHandler('BCH', getBCH))
    updater.dispatcher.add_handler(CommandHandler('ETH', getETH))
    updater.dispatcher.add_handler(CommandHandler('ETC', getETC))
    updater.dispatcher.add_handler(CommandHandler('ZEC', getZEC))

    updater.dispatcher.add_handler(CommandHandler('gainers', gainers))
    updater.dispatcher.add_handler(CommandHandler('losers', losers))

    updater.dispatcher.add_handler(CommandHandler('(A)', changeFilterA))
    updater.dispatcher.add_handler(CommandHandler('(B)', changeFilterB))
    updater.dispatcher.add_handler(CommandHandler('(C)', changeFilterC))
    updater.dispatcher.add_handler(CommandHandler('(D)', changeFilterD))
    updater.dispatcher.add_handler(CommandHandler('(E)', changeFilterE))
    updater.dispatcher.add_handler(CommandHandler('(N)', changeFilterN))

    updater.dispatcher.add_handler(MessageHandler(Filters.text, menu))

    updater.dispatcher.add_error_handler(error)

    _logger.info('bot running...')
    _logger.info('press (ctrl + C) to stop.')
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
# ADD ERROR FUNCTION
