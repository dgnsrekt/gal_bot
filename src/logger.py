from logging import basicConfig, INFO, StreamHandler, getLogger
from datetime import date, datetime
from os import listdir, makedirs, path, remove
from sys import stdout

# Gets basepath of the file
BASE_PATH = path.dirname(path.abspath(__file__))
LOG_PATH = path.join(BASE_PATH, 'logs')


def logFolderExist():
    """Returns True if logging folder exists."""
    return path.exists(LOG_PATH)


def createLogFolder():
    """Creates Log Foler"""
    makedirs(LOG_PATH)


def generateLogNameFromDateTime():
    """Generates the name of a log file from the current time."""
    return 'LOGFILE_({}).log'.format(date.today().isoformat().split(
        '.')[0].replace('T', '_'))


def getDateTimeObjectFromFileName(file):
    """Parses datetime object from a file name."""
    return datetime.strptime(file, 'LOGFILE_(%Y-%m-%d).log')


def deleteOldLogs():
    """Deletes Logs if there are more than 4."""
    while len(listdir(LOG_PATH)) > 4:
        logsFromFolder = listdir(LOG_PATH)
        datetimes = []
        for log in logsFromFolder:
            datetimes.append(getDateTimeObjectFromFileName(log))
        last_log = datetimes.index(min(datetimes))
        remove(path.join(LOG_PATH, logsFromFolder[last_log]))


def generateLogger():
    """Returns a logger object."""
    if not logFolderExist():
        createLogFolder()

    if len(listdir(LOG_PATH)) > 4:
        deleteOldLogs()

    file_name = path.join(LOG_PATH, generateLogNameFromDateTime())
    basicConfig(filename=file_name, level=INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch = StreamHandler(stdout)
    logger = getLogger(__name__)
    logger.addHandler(ch)
    return logger


LOGGER = generateLogger()


def getLogger():
    """Returns a logger instance."""
    return LOGGER

if __name__ == '__main__':
    LOGGER.debug('testing debug...')
    LOGGER.info('testing info...')
    LOGGER.warning('testing warning...')
    LOGGER.error('testing error...')
    LOGGER.critical('testing critical...')
