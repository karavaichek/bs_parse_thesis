import json
import csv
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


with open(f'E:/Thesis/Excel files/Output_dataset/full_dataset.json', 'r') as full_dataset:
    data_set = json.load(full_dataset)

done_flag = False
with tqdm(total=len(full_tickers_list)) as pbar:
    for elem in full_tickers_list:
        tkr = elem
        for i in range(2020, 2024):
            try:
                for fsli in list(data_set[tkr][str(i)]['bs'].keys()):
                    if data_set[tkr][str(i)]['bs'][fsli] is None:
                        data_set[tkr][str(i)]['bs'][fsli]=0
                        print ('changed')
            except KeyError:
                pass
            try:
                for fsli in list(data_set[tkr][str(i)]['pl'].keys()):
                    if data_set[tkr][str(i)]['pl'][fsli] is None:
                        data_set[tkr][str(i)]['pl'][fsli]=0
                        print ('changed')
            except KeyError:
                pass
        done_flag = True
        pbar.update(1)

if done_flag:
    with open(f'E:/Thesis/Excel files/Output_dataset/full_dataset.json', 'w') as f:
        json.dump(data_set, f)
        print ('done')