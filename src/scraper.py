from logger import getLogger
import pickle
import pandas as pd
from os import path

_logger = getLogger()

BASE_PATH = path.dirname(path.abspath(__file__))
PICKLE_PATH = path.join(BASE_PATH, 'pickles')

URL = 'https://coinmarketcap.com/gainers-losers/'


def parseSite(url=URL):
    gainers_losers_dataframe = pd.read_html(url)

    gainers_losers = {
        'gainers_1h': gainers_losers_dataframe[0],
        'gainers_7d': gainers_losers_dataframe[1],
        'gainers_24h': gainers_losers_dataframe[2],
        'losers_1h': gainers_losers_dataframe[3],
        'losers_7d': gainers_losers_dataframe[4],
        'losers_24h': gainers_losers_dataframe[5]}
    _logger.info('Data parsed from {}'.format(url))

    return gainers_losers


def cleanStrings(stringObj):
    return stringObj.replace('$', '').replace(',', '').replace('%', '').replace(' ', '')


def cleanDataFrame(data_frame):
    df = data_frame.copy()
    df.columns = ['#', 'Name', 'Symbol', 'Volume', 'Price', 'Pct']

    df['Name'] = df['Name'].astype(str)
    df['Symbol'] = df['Symbol'].astype(str)
    df['Volume'] = df['Volume'].apply(cleanStrings).astype(int)
    df['Price'] = df['Price'].apply(cleanStrings).astype(float)
    df['Pct'] = df['Pct'].apply(cleanStrings).astype(float)
    return df


def parseAndCleanAllData():
    df = parseSite()

    for key, dfc in df.items():
        df[key] = cleanDataFrame(dfc)
    return df


def filterByVolume(data_frame, min_volume=25000):
    df = data_frame.copy()
    return df[data_frame.Volume > min_volume]


def getFilteredVolumeData():
    temp_df = parseAndCleanAllData()

    volume_NF = {}
    volume_25000 = {}
    volume_100000 = {}
    volume_250000 = {}
    volume_500000 = {}
    volume_1000000 = {}

    for key, df in temp_df.items():
        volume_NF[key] = filterByVolume(
            df, min_volume=0).to_string(index=False)

        volume_25000[key] = filterByVolume(
            df, min_volume=25000).to_string(index=False)

        volume_100000[key] = filterByVolume(
            df, min_volume=100000).to_string(index=False)

        volume_250000[key] = filterByVolume(
            df, min_volume=250000).to_string(index=False)

        volume_500000[key] = filterByVolume(
            df, min_volume=500000).to_string(index=False)

        volume_1000000[key] = filterByVolume(
            df, min_volume=1000000).to_string(index=False)

    return {'A': volume_25000,
            'B': volume_100000,
            'C': volume_250000,
            'D': volume_500000,
            'E': volume_1000000,
            'N': volume_NF}


def createDataPickle(name, data):
    filename = path.join(PICKLE_PATH, name + '.pickle')
    with open(filename, 'wb') as file:
        pickle.dump(data, file)
    _logger.info('{} created.'.format(filename))


def sendDataToPickle(data):
    for x in data:
        createDataPickle(x, data[x])


def getDataFromPickle(filter):
    filename = path.join(PICKLE_PATH, filter.upper() + '.pickle')
    with open(filename, 'rb') as file:
        data = pickle.load(file)
    _logger.info('Pulled data from {}.'.format(filename))
    return data


if __name__ == '__main__':
    data = getFilteredVolumeData()
    sendDataToPickle(data)
