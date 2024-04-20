import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
import json
import csv
from functools import reduce

# Load your dataset into a pandas DataFrame
with open(f'E:/Thesis/Excel files/Output_dataset/full_dataset.json', 'r') as full_dataset:
    data_set = json.load(full_dataset)
data = pd.DataFrame.from_dict(data_set,orient='index', columns=['Revenue', 'COGS', 'EBITDA', 'Op. Revenue', 'Sector', 'Cash', 'inventory',
                               'AR', 'AP', 'Current Debt', 'Current Assets', 'Current Liabilities',
                               'EBITDA Margin', 'CCC'])  # Replace "your_dataset.csv" with the path to your dataset file
#data = data.transpose()
print (data)
# Preprocessing: Depending on your dataset and its characteristics, you might need to perform various preprocessing steps such as handling missing values, encoding categorical variables, scaling numerical features, etc.
# For example:
data.dropna(inplace=True)  # Drop rows with missing values
data = pd.get_dummies(data, columns=['Sector'])

# Splitting data into features and target variable
X = data.drop('CCC', axis=1)
y = data['CCC']

# Splitting data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardizing features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Training the neural network model
model = MLPRegressor(hidden_layer_sizes=(100, 50, 25,10), activation='relu', solver='adam', random_state=42)
model.fit(X_train_scaled, y_train)

# Predicting on the test set
y_pred = model.predict(X_test_scaled)

# Evaluating the model
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)