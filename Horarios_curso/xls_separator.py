import os
import pandas as pd

# Specify the path to your Excel workbook
excel_file = r'C:\Users\diego\OneDrive\Documentos\Pythonhw\.vs\Curricular_analyst_UA\data_CA\Calendario Horarios 202420 FORMATO ANTIGUO (16).xlsx'
output_folder = 'extracted_CSV'

# Create the output directory if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Load the Excel file
xls = pd.ExcelFile(excel_file)

# Loop through each sheet and save it as a CSV in the output folder
for sheet_name in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name)
    # Save the DataFrame to a CSV file in the output folder
    df.to_csv(os.path.join(output_folder, f'{sheet_name}.csv'), index=False)

