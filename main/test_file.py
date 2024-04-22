import json

# Load your dataset into a pandas DataFrame
with open(f'E:/Thesis/Excel files/Output_dataset/full_dataset.json', 'r') as full_dataset:
    data_set = json.load(full_dataset)

keys = data_set.copy().keys()

for elem in keys:
    try:
        if data_set[elem][13] < 0 or 10<data_set[elem][12]<-10:
            data_set.pop(elem)
            print ('popped')
    except KeyError:
        pass

with open(f'E:/Thesis/Excel files/Output_dataset/full_dataset.json', 'w') as write:
    json.dump(data_set,write)
