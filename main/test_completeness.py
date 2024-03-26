import json

with open('E:\Thesis\Excel files\S&P500_tickers.json', 'r') as tickers_json:
    tickers = json.load(tickers_json)

with open(f'E:/Thesis/Excel files/Output_dataset/full_dataset.json', 'r') as full_dataset:
    data_set = json.load(full_dataset)

complete_data ={
    '2020':{},
    '2021':{},
    '2022':{},
    '2023':{}
}

for num in tickers:
    tkr = tickers[str(num)]
    for i in range(2020, 2024):
        try:
            if data_set[tkr][str(i)]['Working Cap Metrics']:
                complete_data[str(i)].update(tkr)
        except KeyError:
            pass
