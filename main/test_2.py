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
X = data.drop(['EBITDA Margin', 'CCC'], axis=1)
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

# Plotting all the decision trees
os.makedirs('E:/Thesis/decision_trees', exist_ok=True)

images = []
for i, tree_in_forest in enumerate(model.estimators_):
    plt.figure(figsize=(20, 10))
    plot_tree(tree_in_forest, feature_names=feature_names, filled=True)
    plt.title(f'Decision Tree {i}')
    png_path = f'E:/Thesis/decision_trees/tree_{i}.png'
    plt.savefig(png_path)
    plt.close()

    # Append the image to the list for GIF creation
    images.append(imageio.imread(png_path))  # Updated function call

# Create and save GIF
gif_path = 'E:/Thesis/decision_trees/decision_trees.gif'
imageio.mimsave(gif_path, images, duration=1)

# Save the last decision tree in 4K resolution
last_tree = model.estimators_[-1]
plt.figure(figsize=(40, 20))  # Larger figure size for higher resolution
plot_tree(last_tree, feature_names=feature_names, filled=True)
plt.title('Last Decision Tree (4K Resolution)')
plt.savefig('E:/Thesis/decision_trees/last_tree_4k.png', dpi=300)  # dpi=300 for higher resolution
plt.close()

print(f"GIF saved at {gif_path}")
print("Last decision tree saved in 4K resolution.")
