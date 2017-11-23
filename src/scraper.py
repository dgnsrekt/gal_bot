import pandas as pd

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

if __name__ == '__main__':
    daba = getFilteredVolumeData()

    print(daba['D']['gainers_1h'])
