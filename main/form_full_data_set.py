import json
import yfinance as yf
from tqdm import tqdm

with open('E:\Thesis\Excel files\S&P500_tickers.json', 'r') as tickers_json:
    tickers = json.load(tickers_json)

new_data = {}
temp = {}
data_set = {}
with tqdm(total=len(tickers)) as pbar:
    for num in tickers:
        tkr = tickers[str(num)]
        temp[tkr] = {}
        company = yf.Ticker(tkr)
        sector = company.info['sector']
        for i in range(2020, 2024):
            temp[tkr][i] = {}
            try:
                with open(f'E:/Thesis/Excel files/Output_bs/{i}/{tkr}_{i}.json', 'r') as bs_raw:
                    bs_dict = json.load(bs_raw)
                    key = list(bs_dict)[0]
                    temp[tkr]['sector'] = sector
                    temp[tkr][i]['bs'] = bs_dict[key]
            except IndexError:
                pass
            try:
                with open(f'E:/Thesis/Excel files/Output_pl/{i}/{tkr}_{i}.json', 'r') as pl_raw:
                    pl_dict = json.load(pl_raw)
                    key = list(pl_dict)[0]
                    temp[tkr][i]['pl'] = pl_dict[key]
            except IndexError:
                pass

            if i == 2023:
                data_set.update(temp)
        pbar.update(1)


'''except KeyError:
    print(tkr, ' working cap calc failed')
if num == 502:
print(data_set)'''

with open(f'E:/Thesis/Excel files/Output_dataset/full_dataset.json', 'w') as f:
    json.dump(data_set, f)
