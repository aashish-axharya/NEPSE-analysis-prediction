##convert data into individual stock files

import os
import pandas as pd
import numpy as np
import csv

# Load the stock data
path = 'scrape/data-old'
files = os.listdir(path)
df = pd.DataFrame()

for file in files:
    df = pd.read_csv(os.path.join(path, file))
    new_df = pd.DataFrame()
    for i in range(len(df)):
        symbol = df['Symbol'][i]
        test_df = df.loc[df['Symbol'] == symbol]
        test_df = test_df.reset_index(drop=True)
        test_df['Date'] = file.split('.')[0]

        with open('scrape/data/individual/' + symbol + '.csv', 'a+') as f:
            test_df.to_csv(f, header=False, index=False)

