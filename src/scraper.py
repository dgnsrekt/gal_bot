import pandas as pd

URL = 'https://coinmarketcap.com/gainers-losers/'

gainers_losers_dataframe = pd.read_html(URL)

gainers_losers = {
    'gainers_1h': gainers_losers_dataframe[0],
    'gainers_7d': gainers_losers_dataframe[1],
    'gainers_24h': gainers_losers_dataframe[2],
    'losers_1h': gainers_losers_dataframe[3],
    'losers_7d': gainers_losers_dataframe[4],
    'losers_24h': gainers_losers_dataframe[5]}


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

for key, df in gainers_losers.items():
    gainers_losers[key] = cleanDataFrame(df)


def filterByVolume(data_frame, min_volume=25000):
    df = data_frame.copy()
    return df[data_frame.Volume > min_volume]

volume_25000 = {}
volume_100000 = {}
volume_250000 = {}
volume_500000 = {}
volume_1000000 = {}
for key, df in gainers_losers.items():
    volume_25000[key] = filterByVolume(df).to_string(
        columns=['#', 'Symbol', 'Pct', 'Volume', 'Price'], index=False)
    volume_100000[key] = filterByVolume(df, min_volume=100000).to_html()
    volume_250000[key] = filterByVolume(df, min_volume=250000).to_json()
    volume_500000[key] = filterByVolume(df, min_volume=500000).to_json()
    volume_1000000[key] = filterByVolume(df, min_volume=1000000).to_json()
