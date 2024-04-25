import json

# Load your dataset into a pandas DataFrame
with open(f'E:/Thesis/Excel files/Output_dataset/full_dataset_raw.json', 'r') as full_dataset:
    data_set = json.load(full_dataset)

keys = data_set.copy().keys()

for elem in keys:
    try:
        if 'SENS'in elem or 'OCX' in elem or 'ACB' in elem or 'MSC' in elem  or 'AC' in elem:
            data_set.pop(elem)
            print('popped anomaly')
        if data_set[elem][13] <= 0: # 1st and 99th percentile boundaries for EBITDA Margin (12) and no negative or 0 CCC - treated as random fluctuations
            data_set.pop(elem)
            print ('popped CCC')
        if data_set[elem][12]==0: # 1st and 99th percentile boundaries for EBITDA Margin (12) and no negative or 0 CCC - treated as random fluctuations
            data_set.pop(elem)
            print ('popped EBITDA')
        if  data_set[elem][12]>=2: # 1st and 99th percentile boundaries for EBITDA Margin (12) and no negative or 0 CCC - treated as random fluctuations
            data_set.pop(elem)
            print ('popped EBITDA')
        if data_set[elem][13] >= 365: # 1st and 99th percentile boundaries for EBITDA Margin (12) and no negative or 0 CCC - treated as random fluctuations
            data_set.pop(elem)
            print ('popped CCC')
        if data_set[elem][4]=='No sector': # 1st and 99th percentile boundaries for EBITDA Margin (12) and no negative or 0 CCC - treated as random fluctuations
            data_set.pop(elem)
            print ('popped sector')
        if data_set[elem][12]<=-2:
            data_set.pop(elem)
            print('popped EBITDA')
    except KeyError:
        continue


with open(f'E:/Thesis/Excel files/Output_dataset/full_dataset.json', 'w') as write:
    json.dump(data_set,write)
