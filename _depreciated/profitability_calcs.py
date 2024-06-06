import json
import csv
from functools import reduce
from tqdm import tqdm
import yfinance as yf

with open('E:\Thesis\Excel files\S&P500_tickers.json', 'r') as tickers_json:
    tickers = json.load(tickers_json)
with open('E:/Thesis/Excel files/tickers.csv', 'r') as full_tickers:
    full_tickers_list = list(reduce(lambda x, y: x + y, list(csv.reader(full_tickers)), []))

for elem in tickers:
    if tickers[elem] in full_tickers_list:
        continue
    else:
        full_tickers_list.extend(tickers[elem])

with open(f'E:/Thesis/Excel files/Output_dataset/full_dataset.json', 'r') as full_dataset:
    data_set = json.load(full_dataset)
with tqdm(total=len(full_tickers_list)) as pbar:
    for elem in full_tickers_list:
        tkr = elem
        yf_ticker = yf.Ticker(tkr)
        try:
            data_set[tkr]['sector'] = yf_ticker.info['sector']
        except KeyError:
            data_set[tkr]['sector'] = 'No sector'
            pass
        for i in range(2020, 2024):
            try:
                if data_set[tkr][str(i)]['pl']['EBITDA'] >= 0 and data_set[tkr][str(i)]['pl']['Op. Revenue'] > 0:
                    data_set[tkr][str(i)]['EBITDA Margin'] = data_set[tkr][str(i)]['pl']['EBITDA']/data_set[tkr][str(i)]['pl']['Op. Revenue']
                else:
                    data_set[tkr][str(i)]['EBITDA Margin'] = 0
            except KeyError:
                pass

        pbar.update(1)
with open(f'E:/Thesis/Excel files/Output_dataset/full_dataset.json', 'w') as f:
    json.dump(data_set, f)
    print('done!')