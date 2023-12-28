import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mysql.connector

# Define your MySQL database connection parameters
mydb = mysql.connector.connect(host="localhost", user="root", passwd="1234",database="thesis")

# Define the SQL query to retrieve the data
query = "SELECT * FROM patient_data"
mycursor = mydb.cursor()
mycursor.execute(query)
data = pd.DataFrame(mycursor.fetchall(), columns=["gender", "age", "hypertension", "heart_disease", "ever_married", "work_type", "Residence_type", "avg_glucose_level", "bmi", "smoking_status", "stroke"])

# Defining the stats summary
summary_stats = data.describe()
print("Summary Stats of Original data\n")
print(summary_stats)
print("\n")

# Defining the correlation matrix
correlation_matrix = data.corr()
print("Correlation matrix of Original data\n")
print(correlation_matrix)
print("\n")

# Defining the stroke count
stroke_counts = data['stroke'].value_counts()
print("Stroke Counts of Original data\n")
print(stroke_counts)
print("\n")


# Defining the skewness of the data
numeric_columns = data.select_dtypes(include=['int64', 'float64'])
skewness = numeric_columns.skew()
print("Skewness of Original data\n")
print(skewness)
print("\n")

#-------------------------------------

# Define the SQL query to retrieve the data
query = "SELECT * FROM patient_data where age >= 65 "
mycursor = mydb.cursor()
mycursor.execute(query)
data = pd.DataFrame(mycursor.fetchall(), columns=["gender", "age", "hypertension", "heart_disease", "ever_married", "work_type", "Residence_type", "avg_glucose_level", "bmi", "smoking_status", "stroke"])

# Defining the stats summary
summary_stats = data.describe()
print("Summary Stats of Original data where age is above or equal to 65\n")
print(summary_stats)
print("\n")

# Defining the correlation matrix
correlation_matrix = data.corr()
print("Correlation matrix of Original data where age is above or equal to 65\n")
print(correlation_matrix)
print("\n")

# Defining the stroke count
stroke_counts = data['stroke'].value_counts()
print("Stroke Counts of Original data where age is above or equal to 65\n")
print(stroke_counts)
print("\n")


# Defining the skewness of the data
numeric_columns = data.select_dtypes(include=['int64', 'float64'])
skewness = numeric_columns.skew()
print("Skewness of Original data where age is above or equal to 65\n")
print(skewness)
print("\n")

#--------------------

# Define the SQL query to retrieve the data
query = "SELECT * FROM patient_data where age < 65 "
mycursor = mydb.cursor()
mycursor.execute(query)
data = pd.DataFrame(mycursor.fetchall(), columns=["gender", "age", "hypertension", "heart_disease", "ever_married", "work_type", "Residence_type", "avg_glucose_level", "bmi", "smoking_status", "stroke"])

# Defining the stats summary
summary_stats = data.describe()
print("Summary Stats of Original data where age is below 65\n")
print(summary_stats)
print("\n")

# Defining the correlation matrix
correlation_matrix = data.corr()
print("Correlation matrix of Original data where age is below 65\n")
print(correlation_matrix)
print("\n")

# Defining the stroke count
stroke_counts = data['stroke'].value_counts()
print("Stroke Counts of Original data where age is below 65\n")
print(stroke_counts)
print("\n")


# Defining the skewness of the data
numeric_columns = data.select_dtypes(include=['int64', 'float64'])
skewness = numeric_columns.skew()
print("Skewness of Original data where age is below o65\n")
print(skewness)
print("\n")

#---------------------

# Define the SQL query to retrieve the data
query = "SELECT * FROM oversampled_patient_data"
mycursor = mydb.cursor()
mycursor.execute(query)
data = pd.DataFrame(mycursor.fetchall(), columns=["gender", "age", "hypertension", "heart_disease", "ever_married", "work_type", "Residence_type", "avg_glucose_level", "bmi", "smoking_status", "stroke"])

# Defining the stats summary
summary_stats = data.describe()
print("Summary Stats of Oversampled data\n")
print(summary_stats)
print("\n")

# Defining the correlation matrix
correlation_matrix = data.corr()
print("Correlation matrix of Oversampled data\n")
print(correlation_matrix)
print("\n")

# Defining the stroke count
stroke_counts = data['stroke'].value_counts()
print("Stroke Counts of Oversampled data\n")
print(stroke_counts)
print("\n")


# Defining the skewness of the data
numeric_columns = data.select_dtypes(include=['int64', 'float64'])
skewness = numeric_columns.skew()
print("Skewness of Oversampled data\n")
print(skewness)
print("\n")


# Define the SQL query to retrieve the data
query = "SELECT * FROM oversampled_patient_data_above_65"
mycursor = mydb.cursor()
mycursor.execute(query)
data = pd.DataFrame(mycursor.fetchall(), columns=["gender", "age", "hypertension", "heart_disease", "ever_married", "work_type", "Residence_type", "avg_glucose_level", "bmi", "smoking_status", "stroke"])

# Defining the stats summary
summary_stats = data.describe()
print("Summary Stats of Oversampled data above 65\n")
print(summary_stats)
print("\n")

# Defining the correlation matrix
correlation_matrix = data.corr()
print("Correlation matrix of Oversampled data above 65\n")
print(correlation_matrix)
print("\n")

# Defining the stroke count
stroke_counts = data['stroke'].value_counts()
print("Stroke Counts of Oversampled data above 65\n")
print(stroke_counts)
print("\n")


# Defining the skewness of the data
numeric_columns = data.select_dtypes(include=['int64', 'float64'])
skewness = numeric_columns.skew()
print("Skewness of Oversampled data above 65\n")
print(skewness)
print("\n")


# Define the SQL query to retrieve the data
query = "SELECT * FROM oversampled_patient_data_below_65"
mycursor = mydb.cursor()
mycursor.execute(query)
data = pd.DataFrame(mycursor.fetchall(), columns=["gender", "age", "hypertension", "heart_disease", "ever_married", "work_type", "Residence_type", "avg_glucose_level", "bmi", "smoking_status", "stroke"])

# Defining the stats summary
summary_stats = data.describe()
print("Summary Stats of Oversampled data below 65\n")
print(summary_stats)
print("\n")

# Defining the correlation matrix
correlation_matrix = data.corr()
print("Correlation matrix of Oversampled data below 65\n")
print(correlation_matrix)
print("\n")

# Defining the stroke count
stroke_counts = data['stroke'].value_counts()
print("Stroke Counts of Oversampled data below 65\n")
print(stroke_counts)
print("\n")


# Defining the skewness of the data
numeric_columns = data.select_dtypes(include=['int64', 'float64'])
skewness = numeric_columns.skew()
print("Skewness of Oversampled data below 65\n")
print(skewness)
print("\n")


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mysql.connector

# Define your MySQL database connection parameters
mydb = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="thesis")

def plot_stroke_counts(data, title):
    plt.figure(figsize=(8, 5))
    sns.countplot(x='stroke', data=data)
    plt.title(title)
    plt.xlabel('Stroke')
    plt.ylabel('Count')
    plt.legend(labels=['No Stroke', 'Stroke'])
    plt.show()

# Original Data - Overall
query = "SELECT * FROM patient_data"
mycursor = mydb.cursor()
mycursor.execute(query)
data = pd.DataFrame(mycursor.fetchall(), columns=["gender", "age", "hypertension", "heart_disease", "ever_married", "work_type", "Residence_type", "avg_glucose_level", "bmi", "smoking_status", "stroke"])
plot_stroke_counts(data, 'Stroke Counts - Original Data (Overall)')

# Original Data - Age >= 65
query = "SELECT * FROM patient_data where age >= 65 "
mycursor = mydb.cursor()
mycursor.execute(query)
data = pd.DataFrame(mycursor.fetchall(), columns=["gender", "age", "hypertension", "heart_disease", "ever_married", "work_type", "Residence_type", "avg_glucose_level", "bmi", "smoking_status", "stroke"])
plot_stroke_counts(data, 'Stroke Counts - Original Data (Age >= 65)')

# Original Data - Age < 65
query = "SELECT * FROM patient_data where age < 65 "
mycursor = mydb.cursor()
mycursor.execute(query)
data = pd.DataFrame(mycursor.fetchall(), columns=["gender", "age", "hypertension", "heart_disease", "ever_married", "work_type", "Residence_type", "avg_glucose_level", "bmi", "smoking_status", "stroke"])
plot_stroke_counts(data, 'Stroke Counts - Original Data (Age < 65)')

# Oversampled Data - Overall
query = "SELECT * FROM oversampled_patient_data"
mycursor = mydb.cursor()
mycursor.execute(query)
data = pd.DataFrame(mycursor.fetchall(), columns=["gender", "age", "hypertension", "heart_disease", "ever_married", "work_type", "Residence_type", "avg_glucose_level", "bmi", "smoking_status", "stroke"])
plot_stroke_counts(data, 'Stroke Counts - Oversampled Data (Overall)')

# Oversampled Data - Age >= 65
query = "SELECT * FROM oversampled_patient_data_above_65"
mycursor = mydb.cursor()
mycursor.execute(query)
data = pd.DataFrame(mycursor.fetchall(), columns=["gender", "age", "hypertension", "heart_disease", "ever_married", "work_type", "Residence_type", "avg_glucose_level", "bmi", "smoking_status", "stroke"])
plot_stroke_counts(data, 'Stroke Counts - Oversampled Data (Age >= 65)')

# Oversampled Data - Age < 65
query = "SELECT * FROM oversampled_patient_data_below_65"
mycursor = mydb.cursor()
mycursor.execute(query)
data = pd.DataFrame(mycursor.fetchall(), columns=["gender", "age", "hypertension", "heart_disease", "ever_married", "work_type", "Residence_type", "avg_glucose_level", "bmi", "smoking_status", "stroke"])
plot_stroke_counts(data, 'Stroke Counts - Oversampled Data (Age < 65)')
