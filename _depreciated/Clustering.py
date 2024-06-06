
import pandas as pd
from sklearn.cluster import BisectingKMeans
import json
import csv
from functools import \
    reduce
import pprint as pprint
import matplotlib.pyplot as plt
import numpy as np

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
    for i in range(2020, 2024):
        tkr = str(elem) + '_' + str(i)
        print (tkr)
        try:
            liquidity_metric_values.append(data_set[tkr][13])
            profit_margin_values.append(data_set[tkr][12])
            COGS_values.append(data_set[tkr][1])
            sector_values.append(data_set[tkr][4])
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

num_clusters = 3

for sector in sectors_list:
    print (sector)
    sector_data = df[df['sector'] == sector]

    # Extract features for clustering
    X = sector_data[['liq', 'prof_mrgn']]

    # Perform clustering
    km = BisectingKMeans(n_clusters=num_clusters)
    km.fit(X)

    # Get cluster labels
    cluster_labels = km.labels_
    results = km.cluster_centers_
    print (results)

    # Print number of observations in each cluster
    for i in range(num_clusters):
        num_obs = np.sum(cluster_labels == i)
        print(f"Cluster {i + 1}: {num_obs} observations")

    plt.figure(figsize=(8, 6))
    for i in range(num_clusters):
        mask = cluster_labels == i
        plt.scatter(X.loc[mask, 'liq'], X.loc[mask, 'prof_mrgn'], label=f'Cluster {i + 1}')

    # Plot decision boundaries
    h = 0.02  # Step size in the mesh
    x_min, x_max = X['liq'].min() - 1, X['liq'].max() + 1
    y_min, y_max = X['prof_mrgn'].min() - 1, X['prof_mrgn'].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    Z = km.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, alpha=0.2, cmap='viridis')

    # Plot centroids
    centroids = km.cluster_centers_
    plt.scatter(centroids[:, 0], centroids[:, 1], marker='o', color='red', edgecolors = 'black' , label='Centroids')

    plt.title(f'Clusters for {sector} sector')
    plt.xlabel('CCC')
    plt.ylabel('EBITDA Margin')
    plt.legend()
    plt.grid(True)
    plt.show()



