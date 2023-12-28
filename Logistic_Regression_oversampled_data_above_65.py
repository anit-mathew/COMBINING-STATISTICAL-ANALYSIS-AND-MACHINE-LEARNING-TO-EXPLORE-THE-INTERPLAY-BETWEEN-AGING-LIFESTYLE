import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
import mysql.connector
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report

# Define your MySQL database connection parameters
mydb = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="thesis")

# Define the SQL query to retrieve the data
query = "SELECT * FROM oversampled_patient_data_above_65"
mycursor = mydb.cursor()
mycursor.execute(query)
data = pd.DataFrame(mycursor.fetchall(), columns=["gender", "age", "hypertension", "heart_disease", "ever_married", "work_type", "Residence_type", "avg_glucose_level", "bmi", "smoking_status", "stroke"])

# Encode categorical variables (work_type and smoking_status)
encoder = LabelEncoder()
categorical_columns = ['gender', 'ever_married', 'work_type', 'Residence_type', 'smoking_status']
for col in categorical_columns:
    data[col] = encoder.fit_transform(data[col])

# Define the features (independent variables) and the target (dependent variable)
features = ['gender', 'hypertension', 'heart_disease', 'ever_married', 'work_type', 'Residence_type', 'avg_glucose_level', 'bmi', 'smoking_status']
target = 'stroke'

X = data[features]
y = data[target]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit a logistic regression model
model = LogisticRegression(solver='liblinear')
model.fit(X_train, y_train)

# Perform cross-validation
cv_results = cross_val_score(model, X, y, cv=5, scoring='accuracy')
print("Cross-Validation Results:")
for i, acc in enumerate(cv_results, 1):
    print(f"Fold {i}: {acc}")

# Make predictions on the test data
y_pred = model.predict(X_test)

# Evaluate the model
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Plot variable importance without underscores and in ascending order
coef_abs = abs(model.coef_[0])
feature_importance = pd.DataFrame({'Feature': features, 'Importance': coef_abs})
feature_importance['Feature'] = feature_importance['Feature'].str.replace('_', ' ')  # Remove underscores
feature_importance = feature_importance.sort_values(by='Importance', ascending=True)

plt.figure(figsize=(10, 6))
plt.barh(feature_importance['Feature'], feature_importance['Importance'])
plt.xlabel('Importance')
plt.title('Variable Importance Plot of Logistic model for above 65')
plt.show()

# Print numerical values of variable importance
print("\nNumerical Values of Variable Importance:")
for feature, importance in zip(feature_importance['Feature'], feature_importance['Importance']):
    print(f"{feature}: {importance}")
