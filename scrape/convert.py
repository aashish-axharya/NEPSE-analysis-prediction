##convert data into individual stock files

import os
import pandas as pd

# Load the stock data
path = 'data'
files = os.listdir(path)

for file in files:
    df = pd.read_csv(os.path.join(path, file))
    test_df = pd.DataFrame(columns=['Name','Conf', 'Open', 'High', 'Low', 'Close', 'VWAP', 'Vol', 'Prev Close', 'Turnover', 'Trans', 'Diff', 'Range', 'Diff Percent', 'Range Percent', 'VWAP%', '120 days','180 days','52 weeks high','52 weeks low'])
    
    # Group the data by symbol and process each group separately
    for symbol, group in df.groupby('Symbol'):
        test_df = group.reset_index(drop=True)
        test_df['Date'] = file.split('.')[0]
        
        # Check if a file already exists for this stock
        file_path = 'individual/{}.csv'.format(symbol)
        try:
            if os.path.isfile(file_path):
                # Append the new data to the existing file
                with open(file_path, 'a') as f:
                    test_df.to_csv(f, header=False, index=False, na_rep='')
            else:
                # Create a new file for the stock
                test_df.to_csv(file_path, index=False, na_rep='')
        except:
            pass

