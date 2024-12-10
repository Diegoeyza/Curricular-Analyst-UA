
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

---------------------------------------------------------------------------------------------------------------

# Database Structure Overview

This document provides a detailed explanation of the database schema for the application. The schema is designed to capture various entities and their relationships, focusing on general entities, objectives, requirements, and RA (Relational Access) links. Below is the breakdown of each table and its structure.

## Table Structure

### courses
- **Purpose**: Stores basic information shared across various entities.
- **Columns**:
  - `id`: A unique identifier for the record.
  - `nombre`: The name associated with the record.

### objectives
- **Purpose**: Captures information related to objectives.
- **Columns**:
  - `id`: A unique identifier that references `courses.id`.
  - `id_objetivo`: The unique ID of the objective.  
  - `nombre`: A name that references `courses.nombre`.  
  - `objetivo`: A detailed description of the objective.
### requirements
- **Purpose**: Links courses records to specific requirements.- **Columns**:  
- `id`: A unique identifier that references `courses.id`.  
- `id_requisito`: A unique identifier that references `course.id`, indicating a requirement.
### ra_links
- **Purpose**: Establishes relationships between courses records, objectives, and prerequisites.
- **Columns**:  
- `id`: A unique identifier that references `courses.id`.  
- `id_objetivo`: References `objectives.id_objetivo`.  
- `id_prerequisito`: References `courses.id`, indicating the prerequisite.  
- `id_objetivo_prerequisito`: References `objectives.id_objetivo`, indicating the objective related to the prerequisite.
- `importancia`: Gives relevance to the link created based on how important it is
## Example Query
To retrieve all RA Links with detailed information, use the following SQL query:

```sql
SELECT 
    rl.id AS ra_link_id,
    g1.nombre AS name,
    o1.objetivo AS objective_description,
    o2.nombre AS prerequisite_name,
    o2.objetivo AS prerequisite_objective_description
FROM 
    ra_links rl
JOIN 
    courses g1 ON rl.id = g1.id
LEFT JOIN 
    objectives o1 ON rl.id_objetivo = o1.id_objetivo
LEFT JOIN 
    courses g2 ON rl.id_prerequisito = g2.id
LEFT JOIN 
    objectives o2 ON rl.id_objetivo_prerequisito = o2.id_objetivo
ORDER BY
    ra_link_id, prerequisite_name DESC;
```

### Explanation of the Query
- **`rl.id AS ra_link_id`**: The unique ID of the RA link.
- **`g1.nombre AS name`**: The name from the courses table for the main record.
- **`o1.objetivo AS objective_description`**: The description of the objective.
- **`o2.nombre AS prerequisite_name`**: The name of the prerequisite.
- **`o2.objetivo AS prerequisite_objective_description`**: The description of the prerequisite objective.
### Joins Used
- **`JOIN courses g1 ON rl.id = g1.id`**: Joins the `courses` table to get the name for the main record.
- **`LEFT JOIN objectives o1 ON rl.id_objetivo = o1.id_objetivo`**: Joins the `objectives` table to get the objective description.
- **`LEFT JOIN courses g2 ON rl.id_prerequisito = g2.id`**: Joins `courses` again to get the prerequisite name.
- **`LEFT JOIN objectives o2 ON rl.id_objetivo_prerequisito = o2.id_objetivo`**: Joins `objectives` to get the prerequisite objective description.
### Ordering
The result is ordered by `ra_link_id` and `prerequisite_name` in descending order.
This schema and query structure provide a comprehensive view of the relationships and entities within the database, allowing easy access to detailed information about RA links and their prerequisites.
