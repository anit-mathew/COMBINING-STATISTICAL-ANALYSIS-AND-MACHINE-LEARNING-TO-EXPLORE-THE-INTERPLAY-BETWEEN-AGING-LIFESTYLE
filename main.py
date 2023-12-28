import pandas as pd
import mysql.connector

# Define your MySQL database connection parameters
mydb = mysql.connector.connect(host="localhost", user="root", passwd="1234",database="thesis")

# Establish a connection to the MySQL database
mycursor = mydb.cursor()

# Creates a new data base
mycursor.execute("DROP DATABASE IF EXISTS thesis")
mycursor.execute("CREATE DATABASE thesis")
mycursor.execute("USE thesis")

# Define the SQL query to create a table
create_table_query = """
        CREATE TABLE IF NOT EXISTS patient_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        gender VARCHAR(10),
        age INT,
        hypertension INT,
        heart_disease INT,
        ever_married VARCHAR(3),
        work_type VARCHAR(20),
        Residence_type VARCHAR(10),
        avg_glucose_level DECIMAL(10, 2),
        bmi DECIMAL(5, 2),
        smoking_status VARCHAR(15),
        stroke INT
        );
        """

mycursor.execute(create_table_query)
mydb.commit()

# Read the CSV file into a pandas DataFrame
csv_file = "full_data.csv"  
data = pd.read_csv(csv_file)

data = data.dropna()

# Insert data from the DataFrame into the MySQL database
for _, row in data.iterrows():
    insert_query = """
        INSERT INTO patient_data
        (gender, age, hypertension, heart_disease, ever_married, work_type, Residence_type, avg_glucose_level, bmi, smoking_status, stroke)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
    mycursor.execute(insert_query, tuple(row))

mydb.commit()
print("Data inserted successfully!")

# Separate features and target variable
X = data.drop('stroke', axis=1)
y = data['stroke']

# Separate the minority and majority classes
minority_class = data[data['stroke'] == 1]
majority_class = data[data['stroke'] == 0]

# Calculate the number of samples needed to balance the classes
minority_count = len(minority_class)
majority_count = len(majority_class)

# Oversample the minority class to match the majority class
oversampled_minority = minority_class.sample(majority_count, replace=True, random_state=42)

# Combine the oversampled minority class with the majority class
oversampled_data = pd.concat([majority_class, oversampled_minority], axis=0)

# Shuffle the combined dataset to mix the samples
oversampled_data = oversampled_data.sample(frac=1, random_state=42).reset_index(drop=True)

# Define the SQL query to create a table
create_table_query = """
        CREATE TABLE IF NOT EXISTS oversampled_patient_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        gender VARCHAR(10),
        age INT,
        hypertension INT,
        heart_disease INT,
        ever_married VARCHAR(3),
        work_type VARCHAR(20),
        Residence_type VARCHAR(10),
        avg_glucose_level DECIMAL(10, 2),
        bmi DECIMAL(5, 2),
        smoking_status VARCHAR(15),
        stroke INT
        );
        """
mycursor.execute(create_table_query)
mydb.commit()


# Insert data from the DataFrame into the MySQL database
for _, row in oversampled_data.iterrows():
    insert_query = """
        INSERT INTO oversampled_patient_data
        (gender, age, hypertension, heart_disease, ever_married, work_type, Residence_type, avg_glucose_level, bmi, smoking_status, stroke)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
    mycursor.execute(insert_query, tuple(row))

mydb.commit()
print("Oversampled Data inserted successfully!")

#Delete Column ID. 
query = '''ALTER TABLE patient_data 
         DROP COLUMN id;'''
        
mycursor = mydb.cursor()
mycursor.execute(query)

#Delete Column ID. 
query = '''ALTER TABLE oversampled_patient_data 
         DROP COLUMN id;'''
        
mycursor = mydb.cursor()
mycursor.execute(query)


# Define the SQL query to retrieve the data
query = "SELECT * FROM patient_data where age >=65"
mycursor = mydb.cursor()
mycursor.execute(query)
data_above_65 = pd.DataFrame(mycursor.fetchall(), columns=["gender", "age", "hypertension", "heart_disease", "ever_married", "work_type", "Residence_type", "avg_glucose_level", "bmi", "smoking_status", "stroke"])


# Separate features and target variable
X = data_above_65.drop('stroke', axis=1)
y = data_above_65['stroke']

# Separate the minority and majority classes
minority_class = data_above_65[data_above_65['stroke'] == 1]
majority_class = data_above_65[data_above_65['stroke'] == 0]

# Calculate the number of samples needed to balance the classes
minority_count = len(minority_class)
majority_count = len(majority_class)

# Oversample the minority class to match the majority class
oversampled_minority = minority_class.sample(majority_count, replace=True, random_state=42)

# Combine the oversampled minority class with the majority class
oversampled_data_above_65 = pd.concat([majority_class, oversampled_minority], axis=0)

# Shuffle the combined dataset to mix the samples
oversampled_data_above_65 = oversampled_data_above_65.sample(frac=1, random_state=42).reset_index(drop=True)

# Define the SQL query to create a table
create_table_query = """
        CREATE TABLE IF NOT EXISTS oversampled_patient_data_above_65 (
        id INT AUTO_INCREMENT PRIMARY KEY,
        gender VARCHAR(10),
        age INT,
        hypertension INT,
        heart_disease INT,
        ever_married VARCHAR(3),
        work_type VARCHAR(20),
        Residence_type VARCHAR(10),
        avg_glucose_level DECIMAL(10, 2),
        bmi DECIMAL(5, 2),
        smoking_status VARCHAR(15),
        stroke INT
        );
        """
mycursor.execute(create_table_query)
mydb.commit()


# Insert data from the DataFrame into the MySQL database
for _, row in oversampled_data_above_65.iterrows():
    insert_query = """
        INSERT INTO oversampled_patient_data_above_65
        (gender, age, hypertension, heart_disease, ever_married, work_type, Residence_type, avg_glucose_level, bmi, smoking_status, stroke)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
    mycursor.execute(insert_query, tuple(row))

mydb.commit()
print("Oversampled Data above 65 inserted successfully!")

#Delete Column ID. 
query = '''ALTER TABLE oversampled_patient_data_above_65
         DROP COLUMN id;'''
        
mycursor = mydb.cursor()
mycursor.execute(query)


# Define the SQL query to retrieve the data
query = "SELECT * FROM patient_data where age < 65"
mycursor = mydb.cursor()
mycursor.execute(query)
data_below_65 = pd.DataFrame(mycursor.fetchall(), columns=["gender", "age", "hypertension", "heart_disease", "ever_married", "work_type", "Residence_type", "avg_glucose_level", "bmi", "smoking_status", "stroke"])


# Separate features and target variable
X = data_below_65.drop('stroke', axis=1)
y = data_below_65['stroke']

# Separate the minority and majority classes
minority_class = data_below_65[data_below_65['stroke'] == 1]
majority_class = data_below_65[data_below_65['stroke'] == 0]

# Calculate the number of samples needed to balance the classes
minority_count = len(minority_class)
majority_count = len(majority_class)

# Oversample the minority class to match the majority class
oversampled_minority = minority_class.sample(majority_count, replace=True, random_state=42)

# Combine the oversampled minority class with the majority class
oversampled_data_below_65 = pd.concat([majority_class, oversampled_minority], axis=0)

# Shuffle the combined dataset to mix the samples
oversampled_data_below_65 = oversampled_data_below_65.sample(frac=1, random_state=42).reset_index(drop=True)

# Define the SQL query to create a table
create_table_query = """
        CREATE TABLE IF NOT EXISTS oversampled_patient_data_below_65 (
        id INT AUTO_INCREMENT PRIMARY KEY,
        gender VARCHAR(10),
        age INT,
        hypertension INT,
        heart_disease INT,
        ever_married VARCHAR(3),
        work_type VARCHAR(20),
        Residence_type VARCHAR(10),
        avg_glucose_level DECIMAL(10, 2),
        bmi DECIMAL(5, 2),
        smoking_status VARCHAR(15),
        stroke INT
        );
        """
mycursor.execute(create_table_query)
mydb.commit()


# Insert data from the DataFrame into the MySQL database
for _, row in oversampled_data_below_65.iterrows():
    insert_query = """
        INSERT INTO oversampled_patient_data_below_65
        (gender, age, hypertension, heart_disease, ever_married, work_type, Residence_type, avg_glucose_level, bmi, smoking_status, stroke)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
    mycursor.execute(insert_query, tuple(row))

mydb.commit()
print("Oversampled Data below 65 inserted successfully!")

#Delete Column ID. 
query = '''ALTER TABLE oversampled_patient_data_below_65
         DROP COLUMN id;'''
        
mycursor = mydb.cursor()
mycursor.execute(query)
mydb.close()


