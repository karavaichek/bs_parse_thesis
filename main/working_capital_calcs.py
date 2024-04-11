import json
import csv
from functools import reduce
from pprint import pprint

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

errors_list = {
    'Working Capital Ratio or turnover':
        {
            '2020': [],
            '2021': [],
            '2022': [],
            '2023': []
        },
    'CCC': {
        '2020': [],
        '2021': [],
        '2022': [],
        '2023': []
    },
    'Total Revenue, Current Assets, Current Liabilities, AR, AP, Inventory для всех лет': []
}

for elem in full_tickers_list:
    tkr = elem
    for i in range(2020, 2024):
        if i % 4 == 0:
            days_in_period = 366
        else:
            days_in_period = 365

        try:
            if i == 2020:
                try:
                    data_set[tkr][str(i)]['Working Cap Metrics'] = {
                        'DIO': data_set[tkr][str(i)]['bs']['Inventory'] / data_set[tkr][str(i)]['pl'][
                            'Cost Of Revenue'] * days_in_period,
                        'DSO': data_set[tkr][str(i)]['bs']['Accounts Receivable'] / data_set[tkr][str(i)]['pl'][
                            'Total Revenue'] * days_in_period,
                        'DPO': data_set[tkr][str(i)]['bs']['Accounts Payable'] / data_set[tkr][str(i)]['pl'][
                            'Total Revenue'] * days_in_period
                    }
                except ZeroDivisionError:
                    pass

            elif i in range(2021, 2024):
                try:
                    data_set[tkr][str(i)]['Working Cap Metrics'] = {
                    'DIO': (data_set[tkr][str(i)]['bs']['Inventory'] - data_set[tkr][str(i - 1)]['bs']['Inventory']) /
                           data_set[tkr][str(i)]['pl']['Cost Of Revenue'] * days_in_period,
                    'DSO': (data_set[tkr][str(i)]['bs']['Accounts Receivable'] - data_set[tkr][str(i - 1)]['bs'][
                        'Accounts Receivable']) / data_set[tkr][str(i)]['pl']['Total Revenue'] * days_in_period,
                    'DPO': (data_set[tkr][str(i)]['bs']['Accounts Payable'] - data_set[tkr][str(i - 1)]['bs'][
                        'Accounts Payable']) /
                           data_set[tkr][str(i)]['pl']['Total Revenue'] * days_in_period
                    }
                except ZeroDivisionError:
                    pass
            try:
                data_set[tkr][str(i)]['Working Cap Metrics']['CCC'] = data_set[tkr][str(i)]['Working Cap Metrics']['DIO'] + \
                                                                  data_set[tkr][str(i)]['Working Cap Metrics']['DSO'] - \
                                                                  data_set[tkr][str(i)]['Working Cap Metrics']['DPO']
            except ZeroDivisionError:
                pass
            print(tkr, ': ', i)
        except KeyError:
            errors_list['CCC'][str(i)] = tkr

with open(f'E:/Thesis/Excel files/Output_dataset/full_dataset.json', 'w') as f:
    json.dump(data_set, f)
    print('done!')
pprint (errors_list)
