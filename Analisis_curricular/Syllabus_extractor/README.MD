# Curriculum Analysis Guide

## Syllabus Processing

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