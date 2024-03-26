import csv
import json

tickers_list = []
tickers_dict = {}

with open('E:\Thesis\Excel files\S&P500_tickers.csv') as csv_file:
    tickers = csv.reader(csv_file)
    for ticker in tickers:
        tickers_list += ticker
    tickers_list.pop(0)

i = 0
for tckr in tickers_list:
    tickers_dict.update({i: tckr})
    i += 1

print(tickers_dict)
with open('E:\Thesis\Excel files\S&P500_tickers.json', 'w') as f:
    json.dump(tickers_dict, f)
