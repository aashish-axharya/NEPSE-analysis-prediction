##convert data into individual stock files

import os
import pandas as pd

# Load the stock data
path = 'scrape/data-old'
files = os.listdir(path)
df = pd.DataFrame()
new_df = pd.DataFrame()

for file in files:
    df = pd.read_csv(os.path.join(path, file))
    test_df = pd.DataFrame(columns=['Name','Conf', 'Open', 'High', 'Low', 'Close', 'VWAP', 'Vol', 'Prev Close', 'Turnover', 'Trans', 'Diff', 'Range', 'Diff Percent', 'Range Percent', 'VWAP%', '120 days','180 days','52 weeks high','52 weeks low'])
    symbol = 'ADBL'
    test_df = df.loc[df['Symbol'] == symbol]
    test_df = test_df.reset_index(drop=True)
    test_df['Date'] = file.split('.')[0]
    new_df = new_df.append(test_df)

new_df.dropna()
with open('scrape/test/' + symbol + '.csv', 'a+') as f:
    new_df.to_csv(f, header=True, index=False)

