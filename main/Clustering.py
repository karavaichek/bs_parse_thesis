import json
import pandas as pd
from sklearn.cluster import KMeans

with open('E:\Thesis\Excel files\S&P500_tickers.json', 'r') as tickers_json:
    tickers = json.load(tickers_json)

with open(f'E:/Thesis/Excel files/Output_dataset/full_dataset.json', 'r') as full_dataset:
    data_set = json.load(full_dataset)


liquidity_metric_values = []
profit_margin_values = []
COGS_values = []
sector_values = []


for num in range(0, len(tickers)):
    tkr = tickers[str(num)]
    for i in range(2020, 2024):
        try:
            liquidity_metric_values.append(data_set[tkr][str(i)]['Working Cap Metrics']['CCC'])
            profit_margin_values.append(data_set[tkr][str(i)]['EBITDA Margin'])
            COGS_values.append(data_set[tkr][str(i)]['pl']['Cost Of Revenue']/pow(10,9))
            sector_values.append(data_set[tkr]['sector'])
        except KeyError:
            pass

d = {'sector':sector_values, 'liq':liquidity_metric_values,'prof_mrgn': profit_margin_values, 'cogs' :COGS_values}
df = pd.DataFrame(data=d)

sectors_list = []
for sector in sector_values:
    if sector in sectors_list:
        continue
    else:
        sectors_list.append(sector)


for sector in sectors_list:
    print (sector)
    km = KMeans(n_clusters=1)
    km.fit(df.loc[df['sector'] == sector, df.columns != 'sector'].to_numpy())
    results = km.cluster_centers_
    print (results)
