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
with tqdm(total=len(full_tickers_list)) as pbar:
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
            try:
                temp[tkr][i] = {}
                with open(f'E:/Thesis/Excel files/Output_bs/{i}/{tkr}_{i}.json', 'r') as bs_raw:
                    bs_dict = json.load(bs_raw)
                    if 'Cash And Cash Equivalents' in list(bs_dict[list(bs_dict)[0]].keys()):
                        try:
                            cash = bs_dict[list(bs_dict)[0]]['Cash And Cash Equivalents']
                        except KeyError:
                            cash = 0
                    else:
                        cash = 0
                    if cash is None:
                        cash = 0
                    if 'Inventory' in list(bs_dict[list(bs_dict)[0]].keys()):
                        try:
                            inventory = bs_dict[list(bs_dict)[0]]['Inventory']
                        except KeyError:
                            inventory = 0
                    else:
                        inventory = 0
                    if inventory is None:
                        inventory = 0
                    if 'Accounts Receivable' in list(bs_dict[list(bs_dict)[0]].keys()):
                        try:
                            accounts_receivable = bs_dict[list(bs_dict)[0]]['Accounts Receivable']
                        except KeyError:
                            accounts_receivable = 0
                    else:
                        accounts_receivable = 0
                    if accounts_receivable is None:
                        accounts_receivable = 0
                    if 'Accounts Payable' in list(bs_dict[list(bs_dict)[0]].keys()):
                        try:
                            accounts_payable = bs_dict[list(bs_dict)[0]]['Accounts Payable']
                        except KeyError:
                            accounts_payable = 0
                    else:
                        accounts_payable = 0
                    if accounts_payable is None:
                        accounts_payable = 0
                    if 'Current Debt' in list(bs_dict[list(bs_dict)[0]].keys()):
                        try:
                            current_debt = bs_dict[list(bs_dict)[0]]['Current Debt']
                        except KeyError:
                            current_debt = 0
                    else:
                        current_debt = 0
                    if current_debt is None:
                        current_debt = 0
                    if 'Current Liabilities' in list(bs_dict[list(bs_dict)[0]].keys()):
                        try:
                            current_liabilities = bs_dict[list(bs_dict)[0]]['Current Liabilities']
                        except KeyError:
                            current_liabilities = 0
                    else:
                        current_liabilities = accounts_payable+current_debt
                    if 'Current Assets' in list(bs_dict[list(bs_dict)[0]].keys()):
                        try:
                            current_assets = bs_dict[list(bs_dict)[0]]['Current Assets']
                        except KeyError:
                            current_assets = 0
                    else:
                        current_assets = cash + inventory + accounts_receivable

                    temp[tkr][i]['bs'] = {'Cash': cash,
                                          'Inv': inventory,
                                          'AR': accounts_receivable,
                                          'AP': accounts_payable,
                                          'Current Debt': current_debt,
                                          'Current Assets': current_assets,
                                          'Current Liabilities':current_liabilities}
            except IndexError:
                pass

            try:
                with open(f'E:/Thesis/Excel files/Output_pl/{i}/{tkr}_{i}.json', 'r') as pl_raw:
                    pl_dict = json.load(pl_raw)
                    if 'Total Revenue' in list(pl_dict[list(pl_dict)[0]].keys()):
                        try:
                            revenue = pl_dict[list(pl_dict)[0]]['Total Revenue']
                        except KeyError:
                            revenue = 0
                    else:
                        revenue = 0
                    if revenue is None:
                        revenue = 0
                    if 'Cost Of Revenue' in list(pl_dict[list(pl_dict)[0]].keys()):
                        try:
                            cost_of_revenue = pl_dict[list(pl_dict)[0]]['Cost Of Revenue']
                        except KeyError:
                            cost_of_revenue = 0
                    else:
                        cost_of_revenue = 0
                    if cost_of_revenue is None:
                        cost_of_revenue = 0
                    if 'Normalized EBITDA' in list(pl_dict[list(pl_dict)[0]].keys()):
                        try:
                            ebitda = pl_dict[list(pl_dict)[0]]['Normalized EBITDA']
                        except KeyError:
                            ebitda = 0
                    else:
                        ebitda = 0
                    if ebitda is None:
                        ebitda = 0
                    if 'Operating Revenue' in list(pl_dict[list(pl_dict)[0]].keys()):
                        try:
                            operating_revenue = pl_dict[list(pl_dict)[0]]['Operating Revenue']
                        except KeyError:
                            operating_revenue = 0
                    else:
                        operating_revenue = 0
                    if operating_revenue is None:
                        operating_revenue = 0

                    temp[tkr][i]['pl'] = {'Revenue': revenue,
                                          'COGS': cost_of_revenue,
                                          'EBITDA': ebitda,
                                          'Op. Revenue': operating_revenue}
            except IndexError:
                pass
            if i == 2023:
                data_set.update(temp)

        pbar.update(1)

with open(f'E:/Thesis/Excel files/Output_dataset/full_dataset.json', 'w') as f:
    json.dump(data_set, f)
