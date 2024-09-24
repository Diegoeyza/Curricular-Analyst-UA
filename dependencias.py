#You first need the csv file from csv converter
import pandas as pd

# Load the CSV files
requisitos_df = pd.read_csv('requirements.csv')  # This file contains ID, ID_Requisito, Nombre_Requisito
general_df = pd.read_csv('general.csv')          # This file contains ID, Nombre

# Step 1: Swap columns in requisitos_df
requisitos_df = requisitos_df.rename(columns={'ID_Requisito': 'ID1'})

# Step 2: Merge with general_df to get the related names
# We need to merge on the 'ID' from requisitos_df and the 'ID' from general_df
result_df = pd.merge(requisitos_df, general_df, on='ID', how='left')

#Renaming columns again to avoid merge issues
result_df = result_df.rename(columns={'ID1': 'ID', 'ID':'ID_Dependencia'})

# Step 3: Rename the 'Nombre' column to 'Dependencia'
result_df = result_df.rename(columns={'Nombre': 'Dependencia'})

# Step 4: Select only the necessary columns
final_df = result_df[['ID', 'ID_Dependencia', 'Dependencia']]

# Step 5: Save the result to a new CSV file
final_df.to_csv('output.csv', index=False)

print("Output file created: output.csv")

