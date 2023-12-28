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
group1['bmi'] = group1['bmi'].astype(float)
group2['bmi'] = group2['bmi'].astype(float)
group3['bmi'] = group3['bmi'].astype(float)

# Extract the 'bmi' column for the ANOVA
bmi_group1 = group1['bmi']
bmi_group2 = group2['bmi']
bmi_group3 = group3['bmi']

# Perform uneven ANOVA on 'bmi'
f_statistic, p_value = f_oneway(bmi_group1, bmi_group2, bmi_group3)

# Print the results
print("F-Statistic:", f_statistic)
print("P-Value:", p_value)

# Check if the p-value is below the significance level (e.g., 0.05) to reject the null hypothesis
if p_value < 0.05:
    print("Reject the null hypothesis: There are significant differences between groups.")
else:
    print("Fail to reject the null hypothesis: No significant differences between groups.")

# Create a box plot for visualization
sns.boxplot(x='Group', y='BMI', data=pd.concat([bmi_group1.rename('BMI').to_frame().assign(Group='Group 1'),
                                               bmi_group2.rename('BMI').to_frame().assign(Group='Group 2'),
                                               bmi_group3.rename('BMI').to_frame().assign(Group='Group 3')]))

# Show the plot
plt.title('BMI Distribution Across Groups')
plt.show()
