import pandas as pd
from openpyxl import load_workbook
import openpyxl
import os

# Function to identify the "UniqueID" column
def find_uniqueid_column(sheet):
    for row in range(4):  # Check rows 0 to 3 (zero-indexed)
        for col, value in enumerate(sheet.iloc[row], start=1):
            if pd.isna(value):
                continue
            if str(value).strip().lower() == "uniqueid":
                return col - 1  # Zero-indexed column
    return None

# Function to read a sheet and preserve formats using openpyxl
def read_excel_with_format(file_path, sheet_name):
    wb = load_workbook(file_path, data_only=True)
    sheet = wb[sheet_name]
    data = sheet.values
    headers = next(data)
    df = pd.DataFrame(data, columns=headers)
    return df

# Load the Excel file and list all sheets
file_path = r"Curricular-Analyst-UA\Evaluación_docente\data\Encuesta Docente Final Semestre Preliminar.xlsx"
output_folder = r"Curricular-Analyst-UA\Evaluación_docente\output"
os.makedirs(output_folder, exist_ok=True)

excel = pd.ExcelFile(file_path)
sheet_names = excel.sheet_names
print("Available sheets:")
for i in range(len(sheet_names)):
    print(sheet_names[i])

# Ask user to select a reference sheet
reference_sheet_name = input("Enter the name of the reference sheet: ")
if reference_sheet_name not in sheet_names:
    raise ValueError("Sheet not found in the Excel file!")

# Read the reference sheet
dataframe = pd.read_excel(file_path, sheet_name=reference_sheet_name)
reference_ids = dataframe.iloc[:, 3].dropna().astype(str)  # Column D (zero-indexed as 3)
reference_categories = dataframe.iloc[:, 1].dropna().astype(str)  # Column B (zero-indexed as 1)

# Validate the reference data
if reference_ids.empty or reference_categories.empty:
    raise ValueError("Reference sheet does not have valid data in columns B or D.")

# Map categories to their respective IDs
category_to_ids = {}
for id_, category in zip(reference_ids, reference_categories):
    category_to_ids.setdefault(category, set()).add(id_)

# Process other sheets
category_dataframes = {category: [] for category in category_to_ids.keys()}

for sheet_name in sheet_names:
    if sheet_name == reference_sheet_name:
        continue

    # Read the sheet and preserve formatting
    sheet = read_excel_with_format(file_path, sheet_name)

    # Find the "UniqueID" column
    uniqueid_col = find_uniqueid_column(sheet)
    if uniqueid_col is None:
        print(f"Skipping sheet '{sheet_name}' (no 'UniqueID' column found).")
        continue

    # Keep all rows but mark rows below "UniqueID" for filtering
    uniqueid_row = sheet.index[sheet.iloc[:, uniqueid_col].str.strip().str.lower() == "uniqueid"].tolist()
    if not uniqueid_row:
        print(f"Skipping sheet '{sheet_name}' (no 'UniqueID' row found).")
        continue

    uniqueid_start_row = uniqueid_row[0]
    retained_header = sheet.iloc[:uniqueid_start_row + 1]  # Keep rows above and including "UniqueID"
    data_rows = sheet.iloc[uniqueid_start_row + 1:]  # Rows after "UniqueID"

    # Filter rows for each category
    for category, ids in category_to_ids.items():
        filtered_rows = data_rows[data_rows.iloc[:, uniqueid_col].isin(ids)]
        if not filtered_rows.empty:
            # Combine retained header and filtered rows
            combined_sheet = pd.concat([retained_header, filtered_rows], ignore_index=True)
            category_dataframes[category].append((sheet_name, combined_sheet))

# Create new Excel files for each category
for category, sheets in category_dataframes.items():
    if not sheets:
        continue

    output_path = os.path.join(output_folder, f"{category}_filtered.xlsx")
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        for sheet_name, filtered_sheet in sheets:
            filtered_sheet.to_excel(writer, sheet_name=sheet_name, index=False)

print("Filtered Excel files created for each category in the specified folder.")
