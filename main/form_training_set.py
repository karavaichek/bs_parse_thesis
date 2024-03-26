import json

with open('E:\Thesis\Excel files\S&P500_tickers.json', 'r') as tickers_json:
    tickers = json.load(tickers_json)

with open(f'E:/Thesis/Excel files/Output_dataset/full_dataset.json', 'r') as full_set:
    temp = json.load(full_set)

new_data = {}
data_set = {}

for num in tickers:
    tkr = tickers[str(num)]
    new_data[tkr] = {}
    for i in range(2020, 2023):
        new_data[tkr][i] = {}
        try:
            new_data[tkr]['sector'] = temp[tkr]['sector']
            new_data[tkr][i]['Working Cap Metrics'] = temp[tkr][str(i)]['Working Cap Metrics']
            new_data[tkr][i]['bs'] = temp[tkr][str(i)]['bs']
        except KeyError:
            pass
        try:
            new_data[tkr][i]['pl'] = temp[tkr][str(i)]['pl']
        except KeyError:
            pass
        if i == 2022:
            print(tkr)
            data_set.update(new_data)

    if num == 502:
        print(data_set)

with open(f'E:/Thesis/Excel files/Output_dataset/training_dataset.json', 'w') as f:
    json.dump(data_set, f)
