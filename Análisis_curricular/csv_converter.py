import csv
import re
import pandas as pd

# Input file path (change this to your file path)
input_file_path = "Extracted_text.txt"

# Read the input data from the file
with open(input_file_path, 'r', encoding='utf-8') as file:
    input_data = file.read()

# Split the input data into blocks for each ID
blocks = input_data.strip().split("\n\n")

# Prepare the output CSV data
general_info = []  # For ID and Nombre
objectives_info = []  # For ID, ID_Objetivo, Objetivo
requirements_info = []  # For ID, ID_Requisito, Nombre_Requisito

# Regular expressions for capturing objectives and requirements
objective_pattern = re.compile(r'(\w+-\d+);(.*)')
requirements_pattern = re.compile(r'ID Requisitos: (.*)')
requirements_name_pattern = re.compile(r'Nombre Requisitos: (.*)')

for block in blocks:
    lines = block.strip().splitlines()
    id_ = ""
    nombre = ""
    objectives = []
    descriptions = []
    id_requisitos = []
    nombre_requisitos = []

    for line in lines:
        if line.startswith("ID="):
            id_ = line.split("=")[1].strip()
        elif line.startswith("Nombre="):
            nombre = line.split("=")[1].strip()
        elif objective_pattern.match(line):
            match = objective_pattern.findall(line)
            for obj_id, description in match:
                objectives.append(obj_id)
                descriptions.append(description.strip())
        elif requirements_pattern.match(line):
            id_requisitos = line.split(":")[1].strip().split(";")
        elif requirements_name_pattern.match(line):
            nombre_requisitos = line.split(":")[1].strip().split(";")

    # Add to general info table
    general_info.append([id_, nombre])
    
    # Append each objective ID and its description to objectives_info
    for obj_id, description in zip(objectives, descriptions):
        objectives_info.append([id_, obj_id, description.strip()])

    # Append each requirement ID and name to requirements_info
    for req_id, req_name in zip(id_requisitos, nombre_requisitos):
        requirements_info.append([id_, req_id.strip(), req_name.strip()])

# Define the CSV output files
general_info_file = "general.csv"
objectives_info_file = "objectives.csv"
requirements_info_file = "requirements.csv"

# Write the general info to CSV
with open(general_info_file, mode='w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["ID", "Nombre"])  # Header
    csv_writer.writerows(general_info)

# Write the objectives info to CSV
with open(objectives_info_file, mode='w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["ID", "ID_Objetivo", "Objetivo"])  # Header
    csv_writer.writerows(objectives_info)

# Write the requirements info to CSV
with open(requirements_info_file, mode='w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["ID", "ID_Requisito", "Nombre_Requisito"])  # Header
    csv_writer.writerows(requirements_info)

print("Data successfully written to CSV files:")
print(f"- {general_info_file}")
print(f"- {objectives_info_file}")
print(f"- {requirements_info_file}")

requirements_df = pd.read_csv(requirements_info_file)  # This file contains ID, ID_Requisito, Nombre_Requisito

# Print the data before filtering for debugging
print("Requirements Data Before Filtering:")
print(requirements_df)

# Filter out rows where 'ID_Requisito' or 'Nombre_Requisito' contains "not found"
requirements_df = requirements_df[~requirements_df['ID_Requisito'].str.strip().str.contains("not found", case=False, na=False)]
requirements_df = requirements_df[~requirements_df['Nombre_Requisito'].str.strip().str.contains("not found", case=False, na=False)]

# Print the filtered data for debugging
print("Filtered Requirements Data:")
print(requirements_df)

# Save the filtered DataFrame back to the requirements_info_file
requirements_df.to_csv(requirements_info_file, index=False)

# Read general_info_file
general_df = pd.read_csv(general_info_file)  # This file contains ID, Nombre

# Step 1: Swap columns in requisitos_df
requirements_df = requirements_df.rename(columns={'ID_Requisito': 'ID1'})

# Step 2: Merge with general_df to get the related names
result_df = pd.merge(requirements_df, general_df, on='ID', how='left')

# Renaming columns again to avoid merge issues
result_df = result_df.rename(columns={'ID1': 'ID', 'ID': 'ID_Dependencia'})

# Step 3: Rename the 'Nombre' column to 'Dependencia'
result_df = result_df.rename(columns={'Nombre': 'Dependencia'})

# Step 4: Select only the necessary columns
final_df = result_df[['ID', 'ID_Dependencia', 'Dependencia']]

# Step 5: Save the result to a new CSV file
final_df.to_csv('dependencies.csv', index=False)

print(f"- dependencies.csv")
