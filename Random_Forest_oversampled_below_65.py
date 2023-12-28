import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import mysql.connector
import matplotlib.pyplot as plt

# Define your MySQL database connection parameters
mydb = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="thesis")

# Define the SQL query to retrieve the data
query = "SELECT * FROM oversampled_patient_data_below_65"
mycursor = mydb.cursor()
mycursor.execute(query)
data = pd.DataFrame(mycursor.fetchall(), columns=["gender", "age", "hypertension", "heart_disease", "ever_married", "work_type", "Residence_type", "avg_glucose_level", "bmi", "smoking_status", "stroke"])

# Remove 'age' from the feature set
X = data.drop(['stroke', 'age'], axis=1)  # Features
y = data['stroke']  # Target variable

# Perform one-hot encoding for categorical features
X = pd.get_dummies(X, columns=['gender', 'ever_married', 'work_type', 'Residence_type', 'smoking_status'])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the Random Forest model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Evaluate the model's performance on the test set
y_pred = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Print a classification report for more detailed metrics
report = classification_report(y_test, y_pred)
print("Random Forest of oversampled data below 65")
print(report)

# Perform k-fold cross-validation using StratifiedKFold
kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_results = cross_val_score(rf_model, X, y, cv=kfold, scoring='accuracy')

# Print the cross-validation results
print("Cross-Validation Results:")
for i, acc in enumerate(cv_results, 1):
    print(f"Fold {i}: {acc}")

# Print the average accuracy across all folds
print(f"Average Accuracy: {cv_results.mean()}")

# Plot variable importance without underscores and in ascending order
feature_importance = rf_model.feature_importances_
features = [col.replace('_', ' ') for col in X.columns]  # Remove underscores
sorted_indices = feature_importance.argsort()

plt.figure(figsize=(10, 6))
plt.barh([features[i] for i in sorted_indices], feature_importance[sorted_indices])
plt.xlabel('Importance')
plt.title('Random Forest Classifier - Variable Importance for below 65')
plt.xticks(rotation=45, ha='right')
plt.show()

# Print the numerical values of variable importance
print("Variable Importance Numerical Values:")
for feature, importance in zip([features[i] for i in sorted_indices], feature_importance[sorted_indices]):
    print(f"{feature}: {importance}")