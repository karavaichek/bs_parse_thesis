import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.tree import plot_tree
import json
import matplotlib.pyplot as plt
import os
import imageio.v2 as imageio  # Updated import

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
X = data.drop(['EBITDA Margin', 'CCC','Current Debt'], axis=1)
y = data[['EBITDA Margin', 'CCC']]

# Splitting data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardizing features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Training the Random Forest model for multi-output regression
model = RandomForestRegressor(n_estimators=10, random_state=42)  # Reduced number of trees for simplicity
model.fit(X_train_scaled, y_train)

# Predicting on the test set
y_pred = model.predict(X_test_scaled)

# Evaluating the model
mse = mean_squared_error(y_test, y_pred, multioutput='raw_values')
print("Mean Squared Error for EBITDA Margin:", mse[0])
print("Mean Squared Error for CCC:", mse[1])

# Extracting feature importances for both targets
feature_importances = model.feature_importances_
feature_names = X.columns

# Separate sectoral features and financial metrics
sectoral_features = [col for col in feature_names if 'Sector' in col]
financial_metrics = [col for col in feature_names if col not in sectoral_features]

# Calculate importances for sectoral features and financial metrics
sectoral_importances = feature_importances[[list(feature_names).index(col) for col in sectoral_features]]
financial_importances = feature_importances[[list(feature_names).index(col) for col in financial_metrics]]

# Create DataFrames for sorting and displaying
sectoral_importance_df = pd.DataFrame(sectoral_importances, index=sectoral_features, columns=['Importance'])
sectoral_importance_df_sorted = sectoral_importance_df.sort_values(by='Importance', ascending=False)

financial_importance_df = pd.DataFrame(financial_importances, index=financial_metrics, columns=['Importance'])
financial_importance_df_sorted = financial_importance_df.sort_values(by='Importance', ascending=False)

print("Sectoral Feature Importances:")
print(sectoral_importance_df_sorted)

print("Financial Metric Importances:")
print(financial_importance_df_sorted)

# Plotting sectoral feature importances
plt.figure(figsize=(10, 6))
plt.barh(sectoral_importance_df_sorted.index, sectoral_importance_df_sorted['Importance'])
plt.xlabel('Importance')
plt.ylabel('Sectoral Features')
plt.title('Sectoral Feature Importances')
plt.savefig('E:/Thesis/sectoral_feature_importances.png')
plt.close()

# Plotting financial metric importances
plt.figure(figsize=(10, 6))
plt.barh(financial_importance_df_sorted.index, financial_importance_df_sorted['Importance'])
plt.xlabel('Importance')
plt.ylabel('Financial Metrics')
plt.title('Financial Metric Importances')
plt.savefig('E:/Thesis/financial_metric_importances.png')
plt.close()


# Input new financial data for prediction
new_data = {
    'Revenue': input ('Revenue'),
    'COGS': input ('COGS'),
    'EBITDA': input ('EBITDA'),
    'Op. Revenue': input ('Op. Revenue'),
    'Sector': input ('Sector'),  # Change this to the relevant sector
    'Cash': input ('Cash'),
    'inventory': input ('inventory'),
    'AR': input ('AR'),
    'AP': input ('AP'),
    'Current Assets': input ('Current Assets'),
    'Current Liabilities': input ('Current Liabilities')
}

# Convert new data to DataFrame
new_data_df = pd.DataFrame(new_data, index=[0])

# Add sector dummy variables to new data
new_data_df = pd.get_dummies(new_data_df, columns=['Sector'])

# Ensure new data has the same dummy variables as the training set
missing_cols = set(data.columns) - set(new_data_df.columns) - {'EBITDA Margin', 'CCC'}
for col in missing_cols:
    new_data_df[col] = 0

# Align the columns of the new data with the training set
new_data_df = new_data_df[X.columns]

# Standardize the new data
new_data_scaled = scaler.transform(new_data_df)

# Predict CCC and EBITDA Margin for the new data
new_predictions = model.predict(new_data_scaled)
predicted_ebitda_margin, predicted_ccc = new_predictions[0]

print(f"Predicted EBITDA Margin: {predicted_ebitda_margin}")
print(f"Predicted CCC: {predicted_ccc}")