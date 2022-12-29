##convert data into individual stock files

import os
import pandas as pd

# Load the stock data
path = 'scrape/data'
files = os.listdir(path)
df = pd.DataFrame()

for file in files:
    df = pd.read_csv(os.path.join(path, file))
    test_df = pd.DataFrame(columns=['SN', 'Symbol','Name','Conf', 'Open', 'High', 'Low', 'Close', 'VWAP', 'Vol', 'Prev Close', 'Turnover', 'Trans', 'Diff', 'Range', 'Diff Percent', 'Range Percent', 'VWAP%', '120 days','180 days','52 weeks high','52 weeks low'])

    for i in range(len(df)):
        symbol = df['Symbol'][i]
        test_df = df.loc[df['Symbol'] == symbol]
        test_df = test_df.reset_index(drop=True)
        test_df['Date'] = file.split('.')[0]

        with open('scrape/test/test/' + symbol + '.csv', 'a+') as f:
            test_df.to_csv(f, header=False, index=False)

