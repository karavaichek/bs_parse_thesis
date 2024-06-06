import json
import csv
from functools import reduce

import pandas as pd
import yfinance as yf
from tqdm import tqdm

with open('E:\Thesis\Excel files\S&P500_tickers.json', 'r') as tickers_json:
    tickers = json.load(tickers_json)
with open('E:/Thesis/Excel files/tickers.csv', 'r') as full_tickers:
    full_tickers_list = list(reduce(lambda x, y: x + y, list(csv.reader(full_tickers)), []))

for elem in tickers:
    if tickers[elem] in full_tickers_list:
        continue
    else:
        full_tickers_list.extend(tickers[elem])

with tqdm(total=len(full_tickers_list)) as pbar:
    for elem in full_tickers_list:
        tkr = elem
        company = yf.Ticker(tkr)
        bs = pd.DataFrame(company.balance_sheet)
        pl = pd.DataFrame(company.income_stmt)
        bs.to_json(f'E:/Thesis/Excel files/Output_bs/raw/{tkr}_bs_raw.json', index=True)
        pl.to_json(f'E:/Thesis/Excel files/Output_pl/raw/{tkr}_pl_raw.json', index=True)

        # 2020
        bs_2020 = bs.filter(regex='2020')
        pl_2020 = pl.filter(regex='2020')
        bs_2020.to_json(f'E:/Thesis/Excel files/Output_bs/2020/{tkr}_2020.json', index=True)
        pl_2020.to_json(f'E:/Thesis/Excel files/Output_pl/2020/{tkr}_2020.json', index=True)

        # 2021
        bs_2021 = bs.filter(regex='2021')
        pl_2021 = pl.filter(regex='2021')
        bs_2021.to_json(f'E:/Thesis/Excel files/Output_bs/2021/{tkr}_2021.json', index=True)
        pl_2021.to_json(f'E:/Thesis/Excel files/Output_pl/2021/{tkr}_2021.json', index=True)

        # 2022
        bs_2022 = bs.filter(regex='2022')
        pl_2022 = pl.filter(regex='2022')
        bs_2022.to_json(f'E:/Thesis/Excel files/Output_bs/2022/{tkr}_2022.json', index=True)
        pl_2022.to_json(f'E:/Thesis/Excel files/Output_pl/2022/{tkr}_2022.json', index=True)

        # 2023
        bs_2023 = bs.filter(regex='2023')
        pl_2023 = pl.filter(regex='2023')
        bs_2023.to_json(f'E:/Thesis/Excel files/Output_bs/2023/{tkr}_2023.json', index=True)
        pl_2023.to_json(f'E:/Thesis/Excel files/Output_pl/2023/{tkr}_2023.json', index=True)

        # progress bar update
        pbar.update(1)