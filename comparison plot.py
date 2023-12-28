import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mysql.connector
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mysql.connector

# Define your MySQL database connection parameters
mydb = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="thesis")

# Define the SQL query to retrieve overall data
query_all = "SELECT * FROM oversampled_patient_data"
mycursor = mydb.cursor()
mycursor.execute(query_all)
data_all = pd.DataFrame(mycursor.fetchall(), columns=["gender", "age", "hypertension", "heart_disease", "ever_married", "work_type", "Residence_type", "avg_glucose_level", "bmi", "smoking_status", "stroke"])

# Define the SQL query to retrieve data where age is above or equal to 65
query_above_65 = "SELECT * FROM oversampled_patient_data_above_65"
mycursor.execute(query_above_65)
data_above_65 = pd.DataFrame(mycursor.fetchall(), columns=["gender", "age", "hypertension", "heart_disease", "ever_married", "work_type", "Residence_type", "avg_glucose_level", "bmi", "smoking_status", "stroke"])

# Define the SQL query to retrieve data where age is below 65
query_below_65 = "SELECT * FROM oversampled_patient_data_below_65"
mycursor.execute(query_below_65)
data_below_65 = pd.DataFrame(mycursor.fetchall(), columns=["gender", "age", "hypertension", "heart_disease", "ever_married", "work_type", "Residence_type", "avg_glucose_level", "bmi", "smoking_status", "stroke"])

# Create subplots with 1 row and 3 columns
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Plot for overall stroke counts
sns.countplot(x='stroke', data=data_all, ax=axes[0])
axes[0].set_title('Stroke Counts - Original Data (Overall)')
axes[0].set_xlabel('Stroke')
axes[0].set_ylabel('Count')
axes[0].legend(labels=['No Stroke', 'Stroke'])

# Plot for stroke counts where age is above or equal to 65
sns.countplot(x='stroke', data=data_above_65, ax=axes[1])
axes[1].set_title('Stroke Counts - Original Data (Age >= 65)')
axes[1].set_xlabel('Stroke')
axes[1].set_ylabel('Count')
axes[1].legend(labels=['No Stroke', 'Stroke'])

# Plot for stroke counts where age is below 65
sns.countplot(x='stroke', data=data_below_65, ax=axes[2])
axes[2].set_title('Stroke Counts - Original Data (Age < 65)')
axes[2].set_xlabel('Stroke')
axes[2].set_ylabel('Count')
axes[2].legend(labels=['No Stroke', 'Stroke'])

# Adjust layout for better visualization
plt.tight_layout()
plt.show()

