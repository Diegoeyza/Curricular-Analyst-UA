
# Curriculum Analysis Guide

## Análisis Curricular

### Steps:
1. **Download and Extract PDFs**:
   - Download all syllabus as PDF files and extract them into a specific folder.

2. **Set Folder Path**:
   - Copy the folder path and update it in `pdf_scrapper` at **line 127**.

3. **Generate Data Tables**:
   - Run `csv_converter` to create tables from the extracted data.

4. **Cross-reference IDs** (Optional):
   - If you need to compare against a file with valid IDs:
     - Convert the file to CSV and ensure the IDs are in a column named `CODIGOS`.
     - Add the file path to **line 4** of `ID_crossreferencer`.
   - When running `ID_crossreferencer`, follow these steps:
     - Choose **Option 1**: This will create `general.csv`, marking each course with a check or cross (indicating whether it should be excluded). Modify this file by removing crosses for courses you want to retain.
     - Run the code again and select **Option 2**: This generates a new table `filtered_general.csv` with the updated course list.
   - Folder filter also helps reduce the number of courses via regular expressions

5. **Upload to Google Sheets**:
   - After getting the CSV with the desired data, it is possible to load it into a Spreadsheet and then use the `Spreadsheet_OA_Linker` folder to create an interactive spreadsheet based on the CSV

---

## Horarios_curso

### Steps:
1. **Prepare the Input File**:
   - Ensure your timetable file has:
     - Days of the week (Monday to Friday) and hours in the first two rows.
     - Course entries in the format: `ELECTRO (LAB) SEC 1;MARTES;9:30;10:20`.
     - **Important**: The course name should:
       - Not contain commas.
       - Have a space between the name and type (e.g., `ELECTRO (CLAS)`).
     - Invalid examples:
       - `ELECTRO(CLAS)` → Missing space.
       - `ELECTRO ( CLAS)` → Extra spaces.

2. **Set File Paths**:
   - Add your timetable file path to **line 5** of [`main.py`](https://github.com/Diegoeyza/Curricular-Analyst-UA/blob/a79c77a4c8fcb8e9cb2623926d34b067f64dffac/Horarios_curso/main.py#L5).
   - Convert your "Programación maestro macro" Excel file to CSV (only the DPSI sheet) and add its path to **line 9** of [`main.py`](https://github.com/Diegoeyza/Curricular-Analyst-UA/blob/a79c77a4c8fcb8e9cb2623926d34b067f64dffac/Horarios_curso/main.py#L9).

3. **Run the Code**:
   - Execute [`main.py`](Horarios_curso/main.py). It will generate:
     - **`Programación Maestro final.csv`**: Updated timetable with assigned schedules (rows without schedules are marked in red).
     - **`Missing_pairs.txt`**: Contains unmatched timetables with their details.

### Not Admitted Formats:
| Incorrect Format                | Correct Format               |
|---------------------------------|------------------------------|
| `SIMULACION (LAB) SEC 1 (LAB )` | `SIMULACION (LAB) SEC 1`     |
| `SIMULACION (LAB) SEC1`         | `SIMULACION (LAB) SEC 1`     |

4. **Modify Equivalences**:
   - Update the dictionary of equivalences in [`iterator.py`](Horarios_curso/iterator.py) as needed:
     - Add new entries.
     - Delete conflicting entries (recommended to recreate the dictionary if necessary).
