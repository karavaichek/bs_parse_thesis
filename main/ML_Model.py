import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Load your dataset into a pandas DataFrame
data = pd.read_csv("your_dataset.csv")  # Replace "your_dataset.csv" with the path to your dataset file

# Preprocessing: Depending on your dataset and its characteristics, you might need to perform various preprocessing steps such as handling missing values, encoding categorical variables, scaling numerical features, etc.
# For example:
# data.dropna(inplace=True)  # Drop rows with missing values
# data = pd.get_dummies(data, columns=['sector'])  # One-hot encode categorical variables

# Splitting data into features and target variable
X = data.drop('working_capital', axis=1)
y = data['working_capital']

# Splitting data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Training the model (Random Forest)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predicting on the test set
y_pred = model.predict(X_test)

# Evaluating the model
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# You can also analyze feature importance
feature_importance = pd.DataFrame(model.feature_importances_, index=X.columns, columns=['Importance'])
print("Feature Importance:\n", feature_importance)