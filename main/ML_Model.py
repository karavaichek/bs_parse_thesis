import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
import json
import csv
from functools import reduce
import matplotlib.pyplot as plt

# Load your dataset into a pandas DataFrame
with open(f'E:/Thesis/Excel files/Output_dataset/full_dataset.json', 'r') as full_dataset:
    data_set = json.load(full_dataset)

data = pd.DataFrame.from_dict(data_set, orient='index', columns=[
    'Revenue', 'COGS', 'EBITDA', 'Op. Revenue', 'Sector', 'Cash', 'inventory',
    'AR', 'AP', 'Current Debt', 'Current Assets', 'Current Liabilities',
    'EBITDA Margin', 'CCC'])

# Preprocessing: Drop rows with missing values
data.dropna(inplace=True)

# Convert categorical variables into dummy/indicator variables
data = pd.get_dummies(data, columns=['Sector'])

# Splitting data into features and target variables
X = data.drop(['EBITDA Margin', 'CCC'], axis=1)
y = data[['EBITDA Margin', 'CCC']]

# Splitting data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardizing features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Training the neural network model for multi-output regression
model = MLPRegressor(hidden_layer_sizes=list(reversed(range(10, 1011, 50))), activation='relu', solver='adam', random_state=42)
model.fit(X_train_scaled, y_train)

# Predicting on the test set
y_pred = model.predict(X_test_scaled)

# Evaluating the model
mse = mean_squared_error(y_test, y_pred, multioutput='raw_values')
print("Mean Squared Error for EBITDA Margin:", mse[0])
print("Mean Squared Error for CCC:", mse[1])

# Visualizing feature importances for both targets
feature_importances = np.abs(model.coefs_[0])
feature_names = X.columns

# Taking the mean importance across neurons for each target
mean_importance_ebitda_margin = feature_importances.mean(axis=1)
mean_importance_ccc = feature_importances.mean(axis=0)

# Printing feature importances in a tabular format for both targets
importance_df_ebitda_margin = pd.DataFrame(mean_importance_ebitda_margin, index=feature_names, columns=['Importance'])
importance_df_ccc = pd.DataFrame(mean_importance_ccc, index=feature_names, columns=['Importance'])

importance_df_sorted_ebitda_margin = importance_df_ebitda_margin.sort_values(by='Importance', ascending=False)
importance_df_sorted_ccc = importance_df_ccc.sort_values(by='Importance', ascending=False)

print("Feature Importances for EBITDA Margin:")
print(importance_df_sorted_ebitda_margin)

print("Feature Importances for CCC:")
print(importance_df_sorted_ccc)

# Plotting feature importances
plt.figure(figsize=(14, 10))
plt.subplot(2, 1, 1)
plt.barh(importance_df_sorted_ebitda_margin.index, importance_df_sorted_ebitda_margin['Importance'])
plt.xlabel('Average Importance')
plt.ylabel('Features')
plt.title('Feature Importances for EBITDA Margin')

plt.subplot(2, 1, 2)
plt.barh(importance_df_sorted_ccc.index, importance_df_sorted_ccc['Importance'])
plt.xlabel('Average Importance')
plt.ylabel('Features')
plt.title('Feature Importances for CCC')

plt.tight_layout()
plt.show()