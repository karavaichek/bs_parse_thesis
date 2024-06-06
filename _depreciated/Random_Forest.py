from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import json
    import pandas as pd

# Load your dataset into a pandas DataFrame
with open(f'E:/Thesis/Excel files/Output_dataset/full_dataset.json', 'r') as full_dataset:
    data_set = json.load(full_dataset)



data = pd.DataFrame.from_dict(data_set,orient='index', columns=['Revenue', 'COGS', 'EBITDA', 'Op. Revenue', 'Sector', 'Cash', 'inventory',
                               'AR', 'AP', 'Current Debt', 'Current Assets', 'Current Liabilities',
                               'EBITDA Margin', 'CCC'])

data.dropna(inplace=True)  # Drop rows with missing values
data = pd.get_dummies(data, columns=['Sector'])
data = data.drop(columns=['EBITDA', 'Revenue', 'Op. Revenue'])

X = data.drop('EBITDA Margin', axis=1)  # Features
y = data['EBITDA Margin']  # Target variable

# Splitting data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Instantiating and training the Random Forest Regressor
rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
rf_regressor.fit(X_train, y_train)

# Predicting on the test set
y_pred = rf_regressor.predict(X_test)

# Evaluating the model
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Extracting feature importance coefficients
feature_importances = rf_regressor.feature_importances_

# Creating a DataFrame to display feature importances
feature_importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': feature_importances})
feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)

# Displaying feature importances
print("\nFeature Importance Coefficients:")
print(feature_importance_df)