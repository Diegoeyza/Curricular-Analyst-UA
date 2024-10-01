import pandas as pd
import csv
from organizer import csv_organizer
from merger import merger
from separator import separator
from combiner import combine

def converter(filename):
    # Read the CSV file with UTF-8 encoding
    df = pd.read_csv(filename, sep=';', header=None, encoding='utf-8')

    # Fill empty cells in the first two columns with the value above them
    df[0] = df[0].ffill()
    df[1] = df[1].ffill()

    # Save the modified DataFrame back to a CSV with UTF-8 encoding
    df.to_csv(filename, sep=';', header=False, index=False, encoding='utf-8')

filename = r'data_CA\horario.csv'

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
df = pd.read_csv(r'data_CA\horario.csv', header=None, sep=';', encoding='utf-8')

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
combine(r"data_CA\Programación Maestro Macro segunda parte.csv","separated_schedule.csv","final.csv")

if second:
    csv_organizer("laboratorios.csv", "lab_filled.csv")
    merger("lab_filled.csv", "lab_merged_schedule.csv")
    separator("lab_merged_schedule.csv", "lab_separated_schedule.csv")
    combine(r"data_CA\Programación Maestro Macro segunda parte.csv","lab_separated_schedule.csv","final.csv")
