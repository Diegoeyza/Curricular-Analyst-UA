import csv
import re

# Input file path (change this to your file path)
input_file_path = "test2.txt"

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
