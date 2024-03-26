import matplotlib.pyplot as plt
import json

with open("E:/Thesis/Excel files/Output_dataset/test_dataset.json", "r") as raw:
    dataset = json.load(raw)

new_data = {}
scatter_data = {}

for tkr in list(dataset.keys()):
    new_data = {tkr:{}}
    try:
        new_data[tkr] = {'Revenue':dataset[tkr]['2023']['pl']['Total Revenue'],
                             'Costs':dataset[tkr]['2023']['pl']['Cost Of Revenue']}
        scatter_data.update(new_data)
        if scatter_data[tkr]['Revenue'] is None:
            del scatter_data[tkr]
    except KeyError:
        pass

with open("E:/Thesis/Excel files/Output_dataset/scatter_data.json", 'w') as f:
    json.dump(scatter_data, f)

for key in list(scatter_data.keys()):
    x = int(scatter_data[key]['Revenue'])/1000000000
    y = int(scatter_data[key]['Costs'])/1000000000
    plt.scatter (x,y)

plt.xlim(0, 25)
plt.ylim(0, 20)
plt.title('Revenue/Costs Scatter')
plt.xlabel('Revenue, bln $')
plt.ylabel('Costs, bln $')
plt.ticklabel_format(style='plain')


plt.show()
