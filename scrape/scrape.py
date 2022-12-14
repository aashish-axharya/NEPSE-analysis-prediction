from bs4 import BeautifulSoup as bs
import requests
import os
import pandas as pd
import logging
import ctypes    

#creating a basic log to check if automation is working
logging.basicConfig(filename='scrape.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
Messagebox = ctypes.windll.user32.MessageBoxW

def scrape():
    # get data from sharesansar and put it in a dataframe
    table = soup.find('table', {'id': 'headFixed'})
    df = pd.DataFrame(columns=['SN', 'Symbol','Name','Conf', 'Open', 'High', 'Low', 'Close', 'VWAP', 'Vol', 'Prev Close', 'Turnover', 'Trans', 'Diff', 'Range', 'Diff Percent', 'Range Percent', 'VWAP%', '120 days','180 days','52 weeks high','52 weeks low'])
    for row in table.find_all('tr'):
        data = row.find_all('td')
        if data:
            sn = data[0].text
            symbol = data[1].find('a').text
            name = data[1].find('a')['title']
            conf = data[2].text
            open = data[3].text
            high = data[4].text
            low = data[5].text
            close = data[6].text
            vwap = data[7].text
            vol = data[8].text
            prev_close = data[9].text
            turnover = data[10].text
            trans = data[11].text
            diff = data[12].text
            range = data[13].text
            diff_percent = data[14].text
            range_percent = data[15].text
            vwap_percent = data[16].text
            days_120 = data[17].text
            days_180 = data[18].text
            weeks_52_high = data[19].text
            weeks_52_low = data[20].text
            insert_row = {'SN': sn, 'Symbol': symbol, 'Name': name, 'Conf': conf, 'Open': open, 'High': high, 'Low': low, 'Close': close, 'VWAP': vwap, 'Vol': vol, 'Prev Close': prev_close, 'Turnover': turnover,'Trans':trans, 'Diff': diff, 'Range': range, 'Diff Percent': diff_percent, 'Range Percent': range_percent, 'VWAP%': vwap_percent, '120 days': days_120, '180 days': days_180, '52 weeks high': weeks_52_high, '52 weeks low': weeks_52_low}
            df1 = pd.DataFrame(insert_row, index=[0])
            df = pd.concat([df,df1], ignore_index=True)
            # df = df.append({'SN': sn, 'Symbol': symbol, 'Name': name, 'Conf': conf, 'Open': open, 'High': high, 'Low': low, 'Close': close, 'VWAP': vwap, 'Vol': vol, 'Prev Close': prev_close, 'Turnover': turnover,'Trans':trans, 'Diff': diff, 'Range': range, 'Diff Percent': diff_percent, 'Range Percent': range_percent, 'VWAP%': vwap_percent, '120 days': days_120, '180 days': days_180, '52 weeks high': weeks_52_high, '52 weeks low': weeks_52_low}, ignore_index=True)
    return df

def to_csv():
    # check if scraping has already been done, if not, use the scrape method and put the contents in a file
            df = scrape()
            df.to_csv(file, index=False)
            logging.debug('Scraping success \n')
            #for windows pop up
            Messagebox(0, "Success", "Scraping", 1)
            
#setting basics
try:
    url = 'https://www.sharesansar.com/today-share-price'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    today = soup.find('span',{'class':'text-org'}).text
    file = f'data/{today}.csv'
    if os.path.exists(file) == False:
        to_csv()
    else:
        print('File already exists')
        logging.debug('Scraping failed, file already exists \n')
        Messagebox(0, "Failed", "Scraping", 1)
except:
    logging.debug('Connection failed')

