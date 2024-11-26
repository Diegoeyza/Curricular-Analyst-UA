
# Curricular Analyst UA - Database Loaders

This project contains scripts for loading various data into the database. The four essential Python scripts in this folder are designed to handle the insertion of key curricular data such as general details, objectives, requirements, and links. 

**Scripts Overview:**
1. **`general_loader.py`**  
   Loads general data into the database.

2. **`objectives_loader.py`**  
   Handles the loading of objectives-related data.

3. **`requirements_loader.py`**  
   Loads requirements data.

4. **`Links_loader.py`**  
   Processes and inserts links-related data.

## Instructions for Use

### Order of Execution
The scripts **must be executed in the specified order**:
1. `general_loader.py`
2. `objectives_loader.py`
3. `requirements_loader.py`
4. `Links_loader.py`

### Important Notes:
- **Error Handling:**  
  If any script encounters errors during data loading:
  1. Fix the problematic data in the source CSV file.
  2. Delete the affected table in the database.
  3. Re-run the corresponding script.  

  ⚠️ Errors will reduce the number of rows loaded into the database, so ensure all errors are resolved before proceeding.

- **CSV File Paths:**  
  Each script requires a specific CSV file as input. Update the corresponding file path in the script to match the location of your data files. For example:
  ```python
  csv_path = "/path/to/your/csv_file.csv"
  ```
  Replace `/path/to/your/csv_file.csv` with the actual path of your data file.

## File Structure
```plaintext
Curricular-Analyst-UA/
└── Análisis_curricular/
    └── Database RA_Links/
        ├── general_loader.py
        ├── objectives_loader.py
        ├── requirements_loader.py
        └── Links_loader.py
```

By following the steps outlined above, you can ensure that the data is successfully loaded into the database.
