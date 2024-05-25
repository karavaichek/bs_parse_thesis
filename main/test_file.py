import json
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import BisectingKMeans
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load your dataset into a pandas DataFrame
with open('E:/Thesis/Excel files/Output_dataset/full_dataset.json', 'r') as full_dataset:
    data_set = json.load(full_dataset)

data = pd.DataFrame.from_dict(data_set, orient='index', columns=[
    'Revenue', 'COGS', 'EBITDA', 'Op. Revenue', 'Sector', 'Cash', 'inventory',
    'AR', 'AP', 'Current Debt', 'Current Assets', 'Current Liabilities',
    'EBITDA Margin', 'CCC'])

# Preprocessing: Drop rows with missing values
data.dropna(inplace=True)

# Store original 'Sector' information for clustering
sectors = data['Sector'].unique()

# Convert categorical variables into dummy/indicator variables
data = pd.get_dummies(data, columns=['Sector'])

# Splitting data into features and target variables
X = data.drop(['EBITDA Margin', 'CCC', 'Current Debt'], axis=1)
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

# Define optimal centroid selection based on highest EBITDA Margin
num_clusters = 3
centroids = {}
optimal_centroids = {}

for sector in sectors:
    sector_data = data[data[f'Sector_{sector}'] == 1]

    # Extract features for clustering
    X_cluster = sector_data[['CCC', 'EBITDA Margin']]

    # Perform clustering
    km = BisectingKMeans(n_clusters=num_clusters)
    km.fit(X_cluster)

    # Get cluster centroids
    sector_centroids = km.cluster_centers_
    centroids[sector] = sector_centroids

    # Find optimal centroid based on highest EBITDA Margin
    optimal_centroid = sector_centroids[np.argmax(sector_centroids[:, 1])]
    optimal_centroids[sector] = optimal_centroid

# Function to calculate EBITDA Margin
def calculate_ebitda_margin(ebitda, revenue):
    return ebitda / revenue if revenue != 0 else 0

# Function to calculate DSO, DPO, DIO, and CCC
def calculate_metrics(ar, ap, inventory, revenue, cogs):
    dso = (ar / revenue) * 365 if revenue != 0 else 0
    dpo = (ap / cogs) * 365 if cogs != 0 else 0
    dio = (inventory / cogs) * 365 if cogs != 0 else 0
    ccc = dso + dio - dpo
    return dso, dpo, dio, ccc

# Function to get user input, predict values, and provide suggestions
def get_user_input():
    new_data = {
        'Revenue': float(entry_revenue.get()),
        'COGS': float(entry_cogs.get()),
        'EBITDA': float(entry_ebitda.get()),
        'Op. Revenue': float(entry_op_revenue.get()),
        'Sector': entry_sector.get(),  # Change this to the relevant sector
        'Cash': float(entry_cash.get()),
        'inventory': float(entry_inventory.get()),
        'AR': float(entry_ar.get()),
        'AP': float(entry_ap.get()),
        'Current Assets': float(entry_current_assets.get()),
        'Current Liabilities': float(entry_current_liabilities.get())
    }

    # Calculate EBITDA Margin
    new_data['EBITDA Margin'] = calculate_ebitda_margin(new_data['EBITDA'], new_data['Revenue'])

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

    # Calculate DSO, DPO, DIO, and CCC for the new data
    dso, dpo, dio, ccc = calculate_metrics(new_data['AR'], new_data['AP'], new_data['inventory'], new_data['Revenue'], new_data['COGS'])

    # Analyze which metric influences CCC the most
    ccc_components = {'DSO': dso, 'DPO': dpo, 'DIO': dio}
    most_influential_metric = max(ccc_components, key=ccc_components.get)

    # Find the optimal centroid for the given sector
    sector = entry_sector.get()
    optimal_centroid = optimal_centroids.get(sector, [0, 0])

    # Calculate distance to optimal centroid
    distance_x = predicted_ccc - optimal_centroid[0]
    distance_y = new_data['EBITDA Margin'] - optimal_centroid[1]

    # Provide suggestions for improvement
    suggestions = f"EBITDA Margin: {new_data['EBITDA Margin']}\n"
    suggestions += f"Predicted CCC: {predicted_ccc}\n"
    suggestions += f"DSO: {dso}\nDPO: {dpo}\nDIO: {dio}\n"
    suggestions += f"Distance to optimal CCC: {distance_x}\n"
    suggestions += f"Distance to optimal EBITDA Margin: {distance_y}\n"
    if distance_y > 0:
        suggestions += "Keep up the good work! Your EBITDA Margin is higher than the optimal point.\n"
    else:
        suggestions += "To improve your EBITDA Margin, consider focusing on the following:\n"
        if most_influential_metric == 'DSO':
            suggestions += " - Improve your DSO by speeding up accounts receivable collections.\n"
        elif most_influential_metric == 'DPO':
            suggestions += " - Improve your DPO by negotiating better terms with suppliers.\n"
        elif most_influential_metric == 'DIO':
            suggestions += " - Improve your DIO by optimizing inventory management.\n"

    messagebox.showinfo("Prediction and Suggestions", suggestions)

# Create the GUI
root = tk.Tk()
root.title("Financial Metrics Prediction")

tk.Label(root, text="Revenue").grid(row=0)
tk.Label(root, text="COGS").grid(row=1)
tk.Label(root, text="EBITDA").grid(row=2)
tk.Label(root, text="Op. Revenue").grid(row=3)
tk.Label(root, text="Sector").grid(row=4)
tk.Label(root, text="Cash").grid(row=5)
tk.Label(root, text="Inventory").grid(row=6)
tk.Label(root, text="AR").grid(row=7)
tk.Label(root, text="AP").grid(row=8)
tk.Label(root, text="Current Assets").grid(row=9)
tk.Label(root, text="Current Liabilities").grid(row=10)

entry_revenue = tk.Entry(root)
entry_cogs = tk.Entry(root)
entry_ebitda = tk.Entry(root)
entry_op_revenue = tk.Entry(root)
entry_sector = tk.Entry(root)
entry_cash = tk.Entry(root)
entry_inventory = tk.Entry(root)
entry_ar = tk.Entry(root)
entry_ap = tk.Entry(root)
entry_current_assets = tk.Entry(root)
entry_current_liabilities = tk.Entry(root)

entry_revenue.grid(row=0, column=1)
entry_cogs.grid(row=1, column=1)
entry_ebitda.grid(row=2, column=1)
entry_op_revenue.grid(row=3, column=1)
entry_sector.grid(row=4, column=1)
entry_cash.grid(row=5, column=1)
entry_inventory.grid(row=6, column=1)
entry_ar.grid(row=7, column=1)
entry_ap.grid(row=8, column=1)
entry_current_assets.grid(row=9, column=1)
entry_current_liabilities.grid(row=10, column=1)

tk.Button(root, text='Predict and Suggest', command=get_user_input).grid(row=11, column=1, pady=4)

root.mainloop()