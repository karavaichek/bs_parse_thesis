import json
import csv
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

with open(f'E:/Thesis/Excel files/Output_dataset/full_dataset.json', 'r') as full_dataset:
    data_set = json.load(full_dataset)

for elem in full_tickers_list:
    tkr = elem
    for i in range(2020, 2024):
        try:
            if data_set[tkr][str(i)]['pl']['Normalized EBITDA'] >= 0 and data_set[tkr][str(i)]['pl']['Operating Revenue'] > 0:
                data_set[tkr][str(i)]['EBITDA Margin'] = data_set[tkr][str(i)]['pl']['Normalized EBITDA']/data_set[tkr][str(i)]['pl']['Operating Revenue']
            else:
                data_set[tkr][str(i)]['EBITDA Margin'] = 0
        except KeyError:
            pass
with open(f'E:/Thesis/Excel files/Output_dataset/full_dataset.json', 'w') as f:
    json.dump(data_set, f)
    print('done!')