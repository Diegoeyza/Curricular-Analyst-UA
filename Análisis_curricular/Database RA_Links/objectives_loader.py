import psycopg2
import csv

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    "dbname=links_ra user=postgres password=bduandes host=localhost port=5432"
)
cur = conn.cursor()

# SQL statement to create the Objectives table
create_objectives_table_sql = """
CREATE TABLE IF NOT EXISTS Objectives (
    ID_Objetivo TEXT PRIMARY KEY, 
    ID TEXT NOT NULL,
    Nombre TEXT NOT NULL,
    Objetivo TEXT NOT NULL,
    FOREIGN KEY (ID) REFERENCES Courses(ID)
);
"""

# Create the Objectives table
cur.execute(create_objectives_table_sql)
conn.commit()
print("Objectives table created successfully.")

# Function to load data into the Objectives table from a CSV file
def load_objectives_from_csv(csv_file):
    error_count = 0  # Counter for rows that could not be added
    count = 0
    count2 = 0
    with open(csv_file, 'r', encoding='utf-8') as f:  # Open the CSV file
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        for row in reader:
            count += 1
            try:
                # Insert data into the Objectives table
                cur.execute(
                    "INSERT INTO Objectives (ID_Objetivo, ID, Nombre, Objetivo) VALUES (%s, %s, %s, %s)",
                    (row[1].strip(), row[0].strip(), row[2].strip(), row[3].strip()),
                )
                count2 += 1  # Increment only after successful insertion
            except psycopg2.errors.UniqueViolation as e:
                conn.rollback()
                print(
                    f"Primary Key violation for row {row}: A record with ID_Objetivo = {row[1]} already exists. Details: {e}"
                )
                error_count += 1
            except psycopg2.errors.ForeignKeyViolation as e:
                conn.rollback()
                print(
                    f"Foreign Key violation for row {row}: The ID = {row[0]} does not exist in the Courses table. Details: {e}"
                )
                error_count += 1
            except psycopg2.IntegrityError as e:
                conn.rollback()
                print(
                    f"Integrity error for row {row}: Check constraints or referential integrity failed. Details: {e}"
                )
                error_count += 1
            except Exception as e:
                conn.rollback()
                print(f"Unexpected error for row {row}: {e}")
                error_count += 1
    conn.commit()
    print(f"Data loaded into the Objectives table from {csv_file}.")
    print(f"Number of rows that could not be added: {error_count}")
    print(f"Total rows processed: {count}")
    print(f"Total rows successfully inserted: {count2}")

# Example usage
csv_file = r"Curricular-Analyst-UA\Análisis_curricular\Database RA_Links\objectives.csv"  # Path to your CSV file
load_objectives_from_csv(csv_file)

# Close the connection
cur.close()
conn.close()
print("Connection closed.")
