import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, f1_score, classification_report
import mysql.connector
import matplotlib.pyplot as plt

# Set seeds for reproducibility
seed = 42
torch.manual_seed(seed)
np.random.seed(seed)

# Define your MySQL database connection parameters
mydb = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="thesis")

# Define the SQL query to retrieve the data
query = "SELECT * FROM oversampled_patient_data"
mycursor = mydb.cursor()
mycursor.execute(query)
data = pd.DataFrame(mycursor.fetchall(), columns=["gender", "age", "hypertension", "heart_disease", "ever_married", "work_type", "Residence_type", "avg_glucose_level", "bmi", "smoking_status", "stroke"])

# Drop 'age' column from the data
data = data.drop(columns=['age'])

# Encode categorical variables using LabelEncoder
label_encoder = LabelEncoder()
categorical_columns = ["gender", "ever_married", "work_type", "Residence_type", "smoking_status"]
for col in categorical_columns:
    data[col] = label_encoder.fit_transform(data[col])

# Split the data into features and target
X = data.drop("stroke", axis=1)
y = data["stroke"]

# Standardize numerical features (avg_glucose_level and bmi)
scaler = StandardScaler()
numerical_features = ["avg_glucose_level", "bmi"]
X[numerical_features] = scaler.fit_transform(X[numerical_features])

# Convert data to PyTorch tensors
X = torch.tensor(X.values, dtype=torch.float32)
y = torch.tensor(y.values, dtype=torch.float32)

# Define the Deep Neural Network (DNN) model
class DNN(nn.Module):
    def __init__(self):
        super(DNN, self).__init__()
        self.fc1 = nn.Linear(in_features=X.shape[1], out_features=64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return torch.sigmoid(x)

# Function to plot variable importance
def plot_variable_importance(model, feature_names):
    if hasattr(model, 'fc1') and isinstance(model.fc1, nn.Linear):
        weights = model.fc1.weight.data.numpy()
        importance = np.abs(weights).mean(axis=0)
        feature_importance = pd.DataFrame({'Feature': feature_names, 'Importance': importance})
        feature_importance['Feature'] = feature_importance['Feature'].str.replace('_', ' ')  # Remove underscores
        feature_importance = feature_importance.sort_values(by='Importance', ascending=True)

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.barh(feature_importance['Feature'], feature_importance['Importance'])
        plt.xlabel('Importance')
        plt.title('Variable Importance Plot of DNN for overall oversampled data')
        plt.savefig('DNN_Model_for_above_65_oversampled_data.png')
        plt.show()

        return feature_importance

# Perform k-fold cross-validation
num_epochs = 100
num_folds = 5
skf = StratifiedKFold(n_splits=num_folds, shuffle=True, random_state=42)

all_y_true = []
all_y_pred = []

for fold, (train_idx, test_idx) in enumerate(skf.split(X, y)):
    print(f"Training on fold {fold + 1}/{num_folds}")
    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]

    # Create the DNN model
    model = DNN()

    # Define the loss function and optimizer
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # Training the model
    for epoch in range(num_epochs):
        model.train()
        optimizer.zero_grad()
        outputs = model(X_train)
        loss = criterion(outputs, y_train.view(-1, 1))
        loss.backward()
        optimizer.step()

    # Evaluate the model
    model.eval()
    with torch.no_grad():
        y_pred = model(X_test)
        y_pred = (y_pred > 0.5).float()

        all_y_true.extend(y_test.numpy())
        all_y_pred.extend(y_pred.numpy())

        accuracy = accuracy_score(y_test.numpy(), y_pred.numpy())
        print(f"Accuracy on test set (fold {fold + 1}): {accuracy}")

# Compute the average classification report
avg_report = classification_report(all_y_true, np.array(all_y_pred) > 0.5)
print(f"Average Classification Report:\n{avg_report}")

# Plot variable importance and print numerical values
feature_importance = plot_variable_importance(model, feature_names=['gender', 'hypertension', 'heart_disease', 'ever_married', 'work_type', 'Residence_type', 'avg_glucose_level', 'bmi', 'smoking_status'])
print("Numerical values of Variable Importance:")
print(feature_importance)
