import pandas as pd
from scipy.stats import f_oneway
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns

# Define your MySQL database connection parameters
mydb = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="thesis")

# Define the SQL query to retrieve the data
query = "SELECT * FROM oversampled_patient_data where stroke = 1"
mycursor = mydb.cursor()
mycursor.execute(query)
group1 = pd.DataFrame(mycursor.fetchall(), columns=["gender", "age", "hypertension", "heart_disease", "ever_married", "work_type", "Residence_type", "avg_glucose_level", "bmi", "smoking_status", "stroke"])

query = "SELECT * FROM oversampled_patient_data_above_65 where stroke = 1"
mycursor = mydb.cursor()
mycursor.execute(query)
group2 = pd.DataFrame(mycursor.fetchall(), columns=["gender", "age", "hypertension", "heart_disease", "ever_married", "work_type", "Residence_type", "avg_glucose_level", "bmi", "smoking_status", "stroke"])

query = "SELECT * FROM oversampled_patient_data_below_65 where stroke = 1"
mycursor = mydb.cursor()
mycursor.execute(query)
group3 = pd.DataFrame(mycursor.fetchall(), columns=["gender", "age", "hypertension", "heart_disease", "ever_married", "work_type", "Residence_type", "avg_glucose_level", "bmi", "smoking_status", "stroke"])

# Convert 'bmi' values to float
group1['avg_glucose_level'] = group1['avg_glucose_level'].astype(float)
group2['avg_glucose_level'] = group2['avg_glucose_level'].astype(float)
group3['avg_glucose_level'] = group3['avg_glucose_level'].astype(float)

# Extract the 'bmi' column for the ANOVA
avg_glucose_level_group1 = group1['avg_glucose_level']
avg_glucose_level_group2 = group2['avg_glucose_level']
avg_glucose_level_group3 = group3['avg_glucose_level']

# Perform uneven ANOVA on 'bmi'
f_statistic, p_value = f_oneway(avg_glucose_level_group1, avg_glucose_level_group2, avg_glucose_level_group3)

# Print the results
print("F-Statistic:", f_statistic)
print("P-Value:", p_value)

# Check if the p-value is below the significance level (e.g., 0.05) to reject the null hypothesis
if p_value < 0.05:
    print("Reject the null hypothesis: There are significant differences between groups.")
else:
    print("Fail to reject the null hypothesis: No significant differences between groups.")

# Create a box plot for visualization
sns.boxplot(x='Group', y='avg_glucose_level', data=pd.concat([avg_glucose_level_group1.rename('avg_glucose_level').to_frame().assign(Group='Group 1'),
                                               avg_glucose_level_group2.rename('avg_glucose_level').to_frame().assign(Group='Group 2'),
                                               avg_glucose_level_group3.rename('avg_glucose_level').to_frame().assign(Group='Group 3')]))

# Show the plot
plt.title('Glucose level Distribution Across Groups')
plt.show()