import pandas as pd

# Read data from the text file
file_path = 'video_schedule.txt'
df = pd.read_csv(file_path)

# Export data to an Excel file
excel_file_path = 'video_schedule.xlsx'
df.to_excel(excel_file_path, index=False)

print(f'Data has been exported to {excel_file_path}')
