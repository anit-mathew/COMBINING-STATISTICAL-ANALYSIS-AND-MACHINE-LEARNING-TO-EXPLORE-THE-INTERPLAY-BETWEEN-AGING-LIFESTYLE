import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Define your MySQL database connection parameters
mydb = mysql.connector.connect(host="localhost", user="root", passwd="1234",database="thesis")

# Define the SQL query to retrieve the data
query = "SELECT * FROM patient_data"
mycursor = mydb.cursor()
mycursor.execute(query)
data = pd.DataFrame(mycursor.fetchall(), columns=["gender", "age", "hypertension", "heart_disease", "ever_married", "work_type", "Residence_type", "avg_glucose_level", "bmi", "smoking_status", "stroke"])

# Create a histogram of age with strokes
plt.figure(figsize=(10, 6))
plt.hist([data[data['stroke'] == 1]['age']], 
         bins=15, alpha=0.7, color=['blue'], label=['Stroke'])

# Add labels and title
plt.title("Distribution of Strokes by Age")
plt.xlabel("Age")
plt.ylabel("Count")
plt.legend()

# Show the plot
plt.show()


# Create a boxplot using Seaborn
plt.figure(figsize=(10, 6))
sns.set(style="whitegrid")
sns.violinplot(x="hypertension", y="age", hue="stroke", data=data, split=True, inner="stick", palette="muted")

# Add labels and title
plt.xlabel("Hypertension")
plt.ylabel("Age")
plt.title("Stroke Distribution by Age and Hypertension")

# Show the plot
plt.legend(title="Stroke", loc="upper right", labels=["No Stroke", "Stroke"])
plt.show()
# Create a bar plot
plt.figure(figsize=(10, 6))
sns.barplot(x="smoking_status", y="stroke", data=data, hue="age", ci=None)
plt.title('Stroke Rate Based on Smoking Status and Age')
plt.xlabel('Smoking Status')
plt.ylabel('Stroke Rate')
plt.legend(title='Age')
plt.show()


# Create age groups
bins = [0, 20, 40, 60, 80, 100]
labels = ['0-20', '21-40', '41-60', '61-80', '81-100']
data['age_group'] = pd.cut(data['age'], bins=bins, labels=labels)

# Calculate stroke rates
gender_age_stroke = data.groupby(['gender', 'age_group'])['stroke'].mean().reset_index()

# Create the plot
plt.figure(figsize=(10, 6))
for gender in data['gender'].unique():
    subset = gender_age_stroke[gender_age_stroke['gender'] == gender]
    plt.plot(subset['age_group'], subset['stroke'], label=gender)

plt.title('Stroke Rate by Gender and Age Group')
plt.xlabel('Age Group')
plt.ylabel('Stroke Rate')
plt.legend()
plt.grid(True)
plt.show()

# Create age groups
age_bins = [0, 30, 50, 70, 100]
age_labels = ['0-30', '30-50', '50-70', '70+']
data['age_group'] = pd.cut(data['age'], bins=age_bins, labels=age_labels)

# Convert categorical columns to strings
data['Residence_type'] = data['Residence_type'].astype(str)
data['age_group'] = data['age_group'].astype(str)

# Group by residence type and age group, and calculate the stroke rate
result = data.groupby(['Residence_type', 'age_group'])['stroke'].mean().reset_index()

# Plot the data
plt.figure(figsize=(10, 6))
plt.bar(result['Residence_type'] + ' - ' + result['age_group'], result['stroke'], color='skyblue')
plt.xlabel('Residence Type - Age Group')
plt.ylabel('Stroke Rate')
plt.title('Stroke Rate by Residence Type and Age Group')
plt.xticks(rotation=45)
plt.show()

# Create age groups
bins = [0, 30, 50, 70, 100]
labels = ['0-30', '31-50', '51-70', '71-100']
data['age_group'] = pd.cut(data['age'], bins=bins, labels=labels)

# Convert 'avg_glucose_level' to float
data['avg_glucose_level'] = data['avg_glucose_level'].astype(float)

# Plot stroke rate by age group and avg_glucose_level
plt.figure(figsize=(12, 6))
sns.boxplot(x='age_group', y='avg_glucose_level', hue='stroke', data=data, palette='Set2')
plt.title('Stroke Rate by Age Group and Average Glucose Level')
plt.xlabel('Age Group')
plt.ylabel('Average Glucose Level')
plt.show()



# Create age groups
age_bins = [0, 18, 40, 60, 100]  # Define age bins as per your preference
age_labels = ["0-18", "19-40", "41-60", "61+"]

data['age_group'] = pd.cut(data['age'], bins=age_bins, labels=age_labels)

# Calculate stroke rates
stroke_rate = data.groupby(['heart_disease', 'age_group'])['stroke'].mean()
print(stroke_rate)

# Plot the data
stroke_rate.unstack().plot(kind='bar')
plt.title('Stroke Rate Based on Heart Disease and Age Groups')
plt.xlabel('Heart Disease')
plt.ylabel('Stroke Rate')
plt.legend(title='Age Group')
plt.show()

# Create bins for BMI and age groups
bmi_bins = [0, 18.5, 24.9, 29.9, 34.9, 100]
bmi_labels = ["Underweight", "Normal", "Overweight", "Obese I", "Obese II"]

age_bins = [0, 18, 25, 40, 50, 65, 100]
age_labels = ["<18", "18-25", "26-40", "41-50", "51-65", "66-100"]

# Apply the bin labels to the DataFrame
data['bmi_group'] = pd.cut(data['bmi'], bins=bmi_bins, labels=bmi_labels)
data['age_group'] = pd.cut(data['age'], bins=age_bins, labels=age_labels)

# Calculate the stroke rate for each group
stroke_rate = data.groupby(['bmi_group', 'age_group'])['stroke'].mean().reset_index()

# Create a pivot table for plotting
pivot_table = stroke_rate.pivot_table(index='bmi_group', columns='age_group', values='stroke')

# Create a heatmap to visualize the stroke rate
plt.figure(figsize=(10, 6))
plt.title('Stroke Rate Based on BMI and Age Groups')
plt.xlabel('Age Group')
plt.ylabel('BMI Group')
plt.imshow(pivot_table, cmap='YlOrRd', interpolation='none', aspect='auto')
plt.colorbar()
plt.xticks(range(len(age_labels)), age_labels, rotation=45)
plt.yticks(range(len(bmi_labels)), bmi_labels)
plt.show()



# Define age groups
age_bins = [0, 20, 40, 60, 80, 100]
age_labels = ['0-20', '21-40', '41-60', '61-80', '81-100']

# Categorize age into age groups
data['age_group'] = pd.cut(data['age'], bins=age_bins, labels=age_labels)

# Calculate stroke rate within each age group and work type
result = data.groupby(['age_group', 'work_type'])['stroke'].mean().unstack()

# Plot the data as a grouped bar chart
result.plot(kind='bar')
plt.title('Stroke Rate by Work Type and Age Group')
plt.xlabel('Age Group')
plt.ylabel('Stroke Rate')
plt.legend(title='Work Type', loc='upper right')
plt.show()

# Filter data for urban and rural areas
urban_data = data[data['Residence_type'] == 'Urban']
rural_data = data[data['Residence_type'] == 'Rural']

# Create subplots
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Plot stroke rate in urban areas by smoking status and age
sns.boxplot(x='smoking_status', y='age', data=urban_data, hue='stroke', ax=axes[0])
axes[0].set_title('Stroke Rate in Urban Areas by Smoking Status')

# Plot stroke rate in rural areas by smoking status and age
sns.boxplot(x='smoking_status', y='age', data=rural_data, hue='stroke', ax=axes[1])
axes[1].set_title('Stroke Rate in Rural Areas by Smoking Status')

# Show the plots
plt.tight_layout()
plt.show()
