import pandas as pd
from scipy.stats import chi2_contingency
import mysql.connector

# Define your MySQL database connection parameters
mydb = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="thesis")

# Define the SQL query to retrieve the data
query = "SELECT * FROM oversampled_patient_data"
mycursor = mydb.cursor()
mycursor.execute(query)
data = pd.DataFrame(mycursor.fetchall(), columns=["gender", "age", "hypertension", "heart_disease", "ever_married", "work_type", "Residence_type", "avg_glucose_level", "bmi", "smoking_status", "stroke"])

# Create a contingency table for 'smoking_status' vs 'stroke'
contingency_table_smoking = pd.crosstab(data['smoking_status'], data['stroke'])

# Perform the chi-square test for 'smoking_status' vs 'stroke'
chi2_smoking, p_smoking, dof_smoking, expected_smoking = chi2_contingency(contingency_table_smoking)

# Print the results for 'smoking_status' vs 'stroke'
print("Chi-Square Statistic (smoking_status vs stroke):", chi2_smoking)
print("p-value (smoking_status vs stroke):", p_smoking)
print("Degrees of Freedom (smoking_status vs stroke):", dof_smoking)
print("Expected Frequencies Table (smoking_status vs stroke):")
print(expected_smoking)
print("\n")

# Create a contingency table for 'age' vs 'stroke'
contingency_table_age = pd.crosstab(data['age'], data['stroke'])

# Perform the chi-square test for 'age' vs 'stroke'
chi2_age, p_age, dof_age, expected_age = chi2_contingency(contingency_table_age)

# Print the results for 'age' vs 'stroke'
print("Chi-Square Statistic (age vs stroke):", chi2_age)
print("p-value (age vs stroke):", p_age)
print("Degrees of Freedom (age vs stroke):", dof_age)
print("Expected Frequencies Table (age vs stroke):")
print(expected_age)
print("\n")

# List of categorical columns (excluding 'stroke')
categorical_columns = ['gender', 'hypertension', 'heart_disease', 'ever_married', 'work_type', 'Residence_type']

# Create an empty dictionary to store the chi-square test results
chi_square_results = {}

# Iterate through categorical columns and perform chi-square tests
for column in categorical_columns:
    contingency_table = pd.crosstab(data[column], data['stroke'])
    chi2, p, dof, expected = chi2_contingency(contingency_table)
    chi_square_results[column] = {'Chi-Square Statistic': chi2, 'p-value': p, 'Degrees of Freedom': dof}

# Print the results for other categorical columns
for column, result in chi_square_results.items():
    print(f"Chi-Square Test for {column} vs. stroke:")
    print("Chi-Square Statistic:", result['Chi-Square Statistic'])
    print("p-value:", result['p-value'])
    print("Degrees of Freedom:", result['Degrees of Freedom'])
    print("\n")
