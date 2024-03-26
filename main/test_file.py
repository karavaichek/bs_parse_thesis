import json

with open(f'E:/Thesis/Excel files/Output_dataset/full_dataset.json', 'r') as full_dataset:
    data_set = json.load(full_dataset)

tickers = ['ACN', 'ADBE', 'AFL', 'ABNB', 'AKAM', 'ARE', 'ALL', 'AXP', 'AIG', 'AMT', 'AMP', 'ANSS', 'AON', 'ACGL', 'AJG',
           'AIZ', 'ADSK', 'ADP', 'AVB', 'BAC', 'BK', 'BRK-B', 'BLK', 'BX', 'BKNG', 'BXP', 'BR', 'BRO', 'CPT', 'COF',
           'CBOE', 'CBRE', 'CNC', 'CHRW', 'SCHW', 'CHTR', 'CB', 'CI', 'CINF', 'C', 'CFG', 'CME', 'CTSH', 'CMCSA', 'CMA',
           'CSGP', 'CCI', 'DAY', 'DLR', 'DFS', 'DG', 'DLTR', 'DHI', 'EBAY', 'EA', 'ELV', 'EPAM', 'EQT', 'EFX', 'EQIX',
           'EQR', 'ETSY', 'EG', 'EXPE', 'EXPD', 'EXR', 'FDS', 'FICO', 'FRT', 'FIS', 'FITB', 'FI', 'FLT', 'FOXA', 'FOX',
           'BEN', 'IT', 'GEN', 'GPN', 'GL', 'GS', 'HIG', 'PEAK', 'HLT', 'HST', 'HUM', 'HBAN', 'ICE', 'IPG', 'INTU',
           'IVZ', 'INVH', 'IQV', 'IRM', 'JKHY', 'J', 'JPM', 'KEY', 'KIM', 'L', 'LOW', 'MTB', 'MKTX', 'MAR', 'MMC', 'MA',
           'MTCH', 'META', 'MET', 'MAA', 'MOH', 'MCO', 'MS', 'MSCI', 'NDAQ', 'NFLX', 'NTRS', 'ODFL', 'ORCL', 'PANW',
           'PAYX', 'PYPL', 'PNC', 'PFG', 'PGR', 'PLD', 'PRU', 'PTC', 'PSA', 'RJF', 'O', 'REG', 'RF', 'RHI', 'SPGI',
           'CRM', 'SBAC', 'NOW', 'SPG', 'STT', 'SYF', 'TROW', 'TSCO', 'TRV', 'TFC', 'TYL', 'USB', 'UBER', 'UDR', 'UNH',
           'VTR', 'VRSN', 'VRSK', 'VICI', 'V', 'WRB', 'WBD', 'WFC', 'WELL', 'WTW', 'YUM', 'ZION']

for tkr in tickers:
    for i in range(2020, 2024):
        if data_set[tkr][str(i)]:
            try:
                data = data_set[tkr][str(i)]['bs']['Current Assets']
            except KeyError:
                print(tkr, 'Current Assets')
            try:
                data = data_set[tkr][str(i)]['bs']['Current Liabilities']
            except KeyError:
                print (tkr, 'Current Liabilities')
            try:
                data = data_set[tkr][str(i)]['pl']['Total Revenue']
            except KeyError:
                print (tkr, 'Total Revenue')
            try:
                data = data_set[tkr][str(i)]['bs']['Accounts Receivable']
            except KeyError:
                print(tkr, 'Accounts Receivable')
            try:
                data = data_set[tkr][str(i)]['bs']['Accounts Payable']
            except KeyError:
                print(tkr, 'Accounts Payable')
            try:
                data = data_set[tkr][str(i)]['bs']['Inventory']
            except KeyError:
                try:
                    data_set[tkr][str(i)]['bs'].update({'Inventory':0})
                except KeyError:
                    pass


with open(f'E:/Thesis/Excel files/Output_dataset/full_dataset.json', 'w') as f:
    json.dump(data_set,f)

