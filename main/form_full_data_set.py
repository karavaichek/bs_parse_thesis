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


new_data = {}
temp = {}
data_set = {}
#with tqdm(total=len(full_tickers_list)) as pbar:
for elem in full_tickers_list:
    tkr = elem
    temp[tkr] = {}
    company = yf.Ticker(tkr)
    try:
        sector = company.info['sector']
        if '404 Client Error' in sector:
            sector = 'No sector'
    except KeyError:
        sector = 'No sector'
        pass

    for i in range(2020, 2024):
        temp[tkr][i] = {}
        try:
            with open(f'E:/Thesis/Excel files/Output_bs/{i}/{tkr}_{i}.json', 'r') as bs_raw:
                bs_dict = json.load(bs_raw)
                if 'Cash And Cash Equivalents' in list(bs_dict[list(bs_dict)[0]].keys())
                    cash = bs_dict[list(bs_dict)[0]]['Cash And Cash Equivalents']
                else:
                    cash = 0
                if 'Inventory' in list(bs_dict[list(bs_dict)[0]].keys())
                    inventory = bs_dict[list(bs_dict)[0]]['Inventory']
                else:
                    inventory = 0
                if 'Accounts Receivable' in list(bs_dict[list(bs_dict)[0]].keys())
                    accounts_receivable = bs_dict[list(bs_dict)[0]]['Accounts Receivable']
                else:
                    accounts_receivable = 0
                if 'Accounts Payable' in list(bs_dict[list(bs_dict)[0]].keys())
                    accounts_payable = bs_dict[list(bs_dict)[0]]['Accounts Payable']
                else:
                    accounts_payable = 0
                if 'Current Debt' in list(bs_dict[list(bs_dict)[0]].keys())
                    current_debt = bs_dict[list(bs_dict)[0]]['Current Debt']
                else:
                    current_debt = 0
                if 'Current Liabilities' in list(bs_dict[list(bs_dict)[0]].keys())
                    current_liabilities = bs_dict[list(bs_dict)[0]]['Current Liabilities']
                else:
                    current_liabilities = accounts_payable+current_debt
                if 'Current Assets' in list(bs_dict[list(bs_dict)[0]].keys())
                    current_assets = bs_dict[list(bs_dict)[0]]['Current Assets']
                else:
                    current_assets = cash + inventory + accounts_receivable


            '''temp[tkr]['sector'] = sector
            temp[tkr][i]['bs'] = bs_dict[key]'''
        except IndexError:
            pass
'''try:
        with open(f'E:/Thesis/Excel files/Output_pl/{i}/{tkr}_{i}.json', 'r') as pl_raw:
            pl_dict = json.load(pl_raw)
            key = list(pl_dict)[0]
            temp[tkr][i]['pl'] = pl_dict[key]
    except IndexError:
        pass

    if i == 2023:
        data_set.update(temp)
pbar.update(1)

with open(f'E:/Thesis/Excel files/Output_dataset/full_dataset.json', 'w') as f:
json.dump(data_set, f)'''
