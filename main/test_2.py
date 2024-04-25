import json

# Load your dataset into a pandas DataFrame
with open(f'E:/Thesis/Excel files/Output_dataset/full_dataset_raw.json', 'r') as full_dataset:
    data_set = json.load(full_dataset)

keys = data_set.copy().keys()

for elem in keys:
    try:
        print (data_set[elem][12])
    except KeyError:
        pass
