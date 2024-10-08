import pandas as pd
import csv
from organizer import csv_organizer
from merger import merger
from separator import separator
from combiner import combine
import os


def xlsx_converter(file,out):
    # Path to the CSV file (this would be the file you have, using a placeholder here)
    csv_file_path = file

    # Reading the CSV file using the correct delimiter
    df = pd.read_csv(csv_file_path, delimiter=';')

    # Create a style function to apply red background for NULL values
    def highlight_null(row):
        # Check if the "DIA" value is NaN or 'NULL'
        if pd.isna(row['DIA']) or row['DIA'] == 'NULL':
            return ['background-color: red'] * len(row)  # Apply red to the entire row
        else:
            return [''] * len(row)  # No highlight for the row



    # Applying the style to the DataFrame
    styled_df = df.style.apply(highlight_null, axis=1)

    # Saving the styled DataFrame to an Excel file
    styled_df.to_excel(out, index=False, engine='openpyxl')



def converter(filename):
    # Read the CSV file with UTF-8 encoding
    df = pd.read_csv(filename, sep=';', header=None, encoding='utf-8')

    # Fill empty cells in the first two columns with the value above them
    df[0] = df[0].ffill()
    df[1] = df[1].ffill()

    # Save the modified DataFrame back to a CSV with UTF-8 encoding
    df.to_csv(filename, sep=';', header=False, index=False, encoding='utf-8')

def convert_row(horario, programación):
    filename = horario

    second = False
    with open(filename, "r", encoding='utf-8') as file:  # Specify UTF-8 encoding
        reader = csv.reader(file)
        header = next(reader)
        limits = []
        counter = 0
        for index, col in enumerate(header):
            for i in range(0, len(col)):
                if col[i] == ";":
                    counter += 1
                    if (((col[i+1] == "L") or (col[i+1] == "l")) and ((col[i+2] == "u") or (col[i+2]) == "U")):
                        limits.append(counter-2)

    # Load the CSV with UTF-8 encoding
    df = pd.read_csv(horario, header=None, sep=';', encoding='utf-8')

    if len(limits) > 0:
        # Select columns for the first section (Lunes to Viernes in the first part)
        first_part = df.iloc[:, limits[0]:7]  # From the first Lunes to the first Viernes (columns 0 to 6)
        # Save the first part to a new CSV
        first_part.to_csv('first_part.csv', index=False, header=False, sep=';', encoding='utf-8')
        converter('first_part.csv')

        if len(limits) > 1:
            # Select columns for the second section (Lunes to Viernes in the second part)
            second_part = df.iloc[:, limits[1]:16]  # From the second Lunes to the second Viernes (columns 9 to 15)
            # Save the second part to a new CSV
            second_part.to_csv('laboratorios.csv', index=False, header=False, sep=';', encoding='utf-8')
            converter('laboratorios.csv')
            second = True

    print("CSV files created: first_part.csv and laboratorios.csv if it corresponds")

    # Pass the UTF-8 encoded files to your organizer, merger, and separator functions
    csv_organizer("first_part.csv", "filled.csv")
    merger("filled.csv", "merged_schedule.csv")
    separator("merged_schedule.csv", "separated_schedule.csv")
    combine(programación,"separated_schedule.csv","final.csv","missing_pairs.txt")
    xlsx_converter("final.csv","final_x.xlsx")

    if second:
        csv_organizer("laboratorios.csv", "lab_filled.csv")
        merger("lab_filled.csv", "lab_merged_schedule.csv")
        separator("lab_merged_schedule.csv", "lab_separated_schedule.csv")
        combine(programación,"lab_separated_schedule.csv","final.csv","missing_pairs.txt")

def delete_files(file_list):
    for file_path in file_list:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            else:
                print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

def process_folder(folder,destination):
    delete_files(["filled.csv","final.csv","first_part.csv","merged_schedule.csv",
    "separated_schedule.csv","final.csv","missing_pairs.txt","final_x.xlsx","laboratorios.csv","lab_filled.csv","lab_merged_schedule.csv","lab_separated_schedule.csv"])

    # Iterate through each file in the specified folder
    for root, dirs, files in os.walk(folder):
        for file in files:
            # Get the full path of the file
            file_path = os.path.join(root, file)
            print(f"\nProcessing {file_path}\n")
            convert_row(file_path,destination)
    delete_files(["filled.csv","final.csv","first_part.csv","merged_schedule.csv",
    "separated_schedule.csv","final.csv","laboratorios.csv","lab_filled.csv","lab_merged_schedule.csv","lab_separated_schedule.csv"])

convert_row(r"extracted_CSV\Semestres IX, X y XI.csv",r"data_CA\Programación Maestro Macro segunda parte.csv")