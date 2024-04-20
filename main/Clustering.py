
import pandas as pd
from sklearn.cluster import KMeans
import json
import csv
from functools import reduce
import pprint as pprint

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

liquidity_metric_values = []
profit_margin_values = []
COGS_values = []
sector_values = []

for elem in full_tickers_list:
    tkr = str(elem)
    print (tkr)
    for i in range(2020, 2024):
        i = str(i)
        try:
            liquidity_metric_values.append(data_set[tkr][i]['Working Cap Metrics']['CCC'])
            profit_margin_values.append(data_set[tkr][i]['EBITDA Margin'])
            COGS_values.append(data_set[tkr][i]['pl']['COGS'] / pow(10, 9))
            sector_values.append(data_set[tkr]['sector'])
        except KeyError:
            print('Key error: ', tkr)
            pass

d = {'sector':sector_values, 'liq':liquidity_metric_values,'prof_mrgn': profit_margin_values, 'cogs' :COGS_values}
df = pd.DataFrame(data=d)


sectors_list = []
sectors_number = {}
for sector in sector_values:
    if sector in sectors_list:
        sectors_number.update({sector: sector_values.count(sector)})
        continue
    else:
        sectors_list.append(sector)
print(sectors_number)

#pprint(df.loc[df['sector'] == sector, df.columns != 'sector'].to_numpy())


for sector in sectors_list:
    print (sector)
    km = KMeans(n_clusters=5)
    km.fit(df.loc[df['sector'] == sector, df.columns != 'sector'].to_numpy())
    results = km.cluster_centers_
    print (results)
