import json

# Load your dataset into a pandas DataFrame
with open(f'E:/Thesis/Excel files/Output_dataset/full_dataset.json', 'r') as full_dataset:
    data_set = json.load(full_dataset)

keys = data_set.copy().keys()

for elem in keys:
    try:
        if data_set[elem][13] <= 0 or data_set[elem][13] >= 365 or 1<data_set[elem][12]<-1 or data_set[elem][4]=='No sector': # 1st and 99th percentile boundaries for EBITDA Margin (12) and no negative or 0 CCC - treated as random fluctuations
            data_set.pop(elem)
            print ('popped')
    except KeyError:
        pass

with open(f'E:/Thesis/Excel files/Output_dataset/full_dataset.json', 'w') as write:
    json.dump(data_set,write)
