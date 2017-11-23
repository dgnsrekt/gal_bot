import pandas as pd


URL = 'https://coinmarketcap.com/gainers-losers/'

gainers_losers_dataframe = pd.read_html(URL)

# gainers_1h = gainers_losers_dataframe[0]
# gainers_7d = gainers_losers_dataframe[1]
# gainers_24h = gainers_losers_dataframe[2]
# losers_1h = gainers_losers_dataframe[3]
# losers_7d = gainers_losers_dataframe[4]
# losers_24h = gainers_losers_dataframe[5]


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

for df in gainers_losers_dataframe:
    print(cleanDataFrame(df))
