import json
import csv
import yfinance as yf
from tqdm import tqdm
from functools import reduce

with open('E:\Thesis\Excel files\S&P500_tickers.json', 'r') as tickers_json:
    tickers = json.load(tickers_json)
with open('E:/Thesis/Excel files/tickers.csv', 'r') as full_tickers:
    full_tickers_list = list(reduce(lambda x, y: x + y, list(csv.reader(full_tickers)), []))

for elem in tickers:
    if tickers[elem] in full_tickers_list:
        continue
    else:
        full_tickers_list.extend(tickers[elem])

with open(f'E:/Thesis/Excel files/Output_dataset/full_dataset.json', 'r') as full_set:
    temp = json.load(full_set)

new_data = {}
data_set = {}

with tqdm(total=len(full_tickers_list)) as pbar:
    for elem in full_tickers_list:
        tkr = elem
        new_data[tkr] = {}
        for i in range(2023, 2024):
            new_data[tkr][i] = {}
            try:
                new_data[tkr][i]['bs'] = temp[tkr][str(i)]['bs']
                new_data[tkr][i]['Working Cap Metrics']=temp[tkr][str(i)]['Working Cap Metrics']
                new_data[tkr]['sector'] = temp[tkr]['sector']
                new_data[tkr][i]['EBITDA Margin'] = temp[tkr][str(i)]['EBITDA Margin']
            except KeyError:
                pass
            try:
                new_data[tkr][i]['pl'] = temp[tkr][str(i)]['pl']
            except KeyError:
                pass
            data_set.update(new_data)
        pbar.update(1)


with open(f'E:/Thesis/Excel files/Output_dataset/test_dataset.json', 'w') as f:
    json.dump(data_set, f)
