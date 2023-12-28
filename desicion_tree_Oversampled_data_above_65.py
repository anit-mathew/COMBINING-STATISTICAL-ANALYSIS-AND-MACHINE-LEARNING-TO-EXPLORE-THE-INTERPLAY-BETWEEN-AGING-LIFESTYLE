import mysql.connector
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

# Define your MySQL database connection parameters
mydb = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="thesis")

# Define the SQL query to retrieve the data
query = "SELECT * FROM oversampled_patient_data_above_65"
mycursor = mydb.cursor()
mycursor.execute(query)
data = pd.DataFrame(mycursor.fetchall(), columns=["gender", "age", "hypertension", "heart_disease", "ever_married", "work_type", "Residence_type", "avg_glucose_level", "bmi", "smoking_status", "stroke"])

# Drop 'age' column from the data
data = data.drop(columns=['age'])

label_encoder = LabelEncoder()
categorical_columns = ['gender', 'ever_married', 'work_type', 'Residence_type', 'smoking_status']
for column in categorical_columns:
    data[column] = label_encoder.fit_transform(data[column])
X = data.drop(columns=['stroke'])
y = data['stroke']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Decision Tree Classifier with regularization parameters
clf = DecisionTreeClassifier(random_state=42, max_depth=5, min_samples_split=5, min_samples_leaf=5)

# Perform k-fold cross-validation (let's say k=5 for example)
cv_scores = cross_val_score(clf, X_train, y_train, cv=5)

# Train the model on the entire training set
clf.fit(X_train, y_train)

# Make predictions on the test set
y_pred = clf.predict(X_test)

# Calculate accuracy, confusion matrix, and classification report
accuracy = accuracy_score(y_test, y_pred)
confusion = confusion_matrix(y_test, y_pred)
classification_report = classification_report(y_test, y_pred)

# Plot feature importance in ascending order horizontally
feature_importance = clf.feature_importances_
features = X.columns
features_without_underscore = [col.replace('_', ' ') for col in features]  # Remove underscores from feature names

# Sort feature importance in ascending order
sorted_indices = feature_importance.argsort()
sorted_features = [features_without_underscore[i] for i in sorted_indices]
sorted_importance = feature_importance[sorted_indices]

plt.barh(sorted_features, sorted_importance)  # Change 'bar' to 'barh'
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.title('Decision Tree Classifier - Feature Importance for above 65')
plt.show()

print("Result of oversampled data above 65\n")
print(f'Accuracy: {accuracy}')
print(f'Confusion Matrix:\n{confusion}')
print(f'Classification Report:\n{classification_report}')
print(f'Cross-Validation Scores: {cv_scores}')
print(f'Mean Cross-Validation Score: {cv_scores.mean()}')

# Print feature names and their importance scores
print("\nNumerical Values of Variable Importance:")
for feature, importance in zip(sorted_features, sorted_importance):
    print(f'{feature}: {importance}')
