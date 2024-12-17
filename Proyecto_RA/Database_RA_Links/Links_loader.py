import psycopg2
import csv

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    "dbname=links_ra user=postgres password=bduandes host=localhost port=5432"
)
cur = conn.cursor()

# SQL statement to create the RA_Links table
create_ra_links_table_sql = """
CREATE TABLE IF NOT EXISTS RA_Links (
    ID TEXT NOT NULL,
    ID_Objetivo TEXT NOT NULL,
    Importancia TEXT NOT NULL,
    ID_Prerrequisito TEXT,
    ID_Objetivo_Prerrequisito TEXT,
    FOREIGN KEY (ID) REFERENCES Courses(ID),
    FOREIGN KEY (ID_Objetivo) REFERENCES Objectives(ID_Objetivo),
    FOREIGN KEY (ID_Prerrequisito) REFERENCES Courses(ID),
    FOREIGN KEY (ID_Objetivo_Prerrequisito) REFERENCES Objectives(ID_Objetivo),
    PRIMARY KEY (ID, ID_Objetivo, ID_Prerrequisito, ID_Objetivo_Prerrequisito)
);
"""

# Create the RA_Links table
cur.execute(create_ra_links_table_sql)
conn.commit()
print("RA_Links table created successfully.")

# Function to load data into the RA_Links table from a CSV file
def load_ra_links_from_csv(csv_file):
    error_count = 0  # Counter for rows that could not be added
    count = 0
    count2 = 0
    with open(csv_file, 'r', encoding='utf-8') as f:  # Open the CSV file
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        for row in reader:
            count += 1
            try:
                # Insert data into the RA_Links table
                cur.execute(
                    """
                    INSERT INTO RA_Links (
                        ID, ID_Objetivo, Importancia, ID_Prerequisito, ID_Objetivo_Prerequisito
                    ) VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        row[0].strip(),  # ID
                        row[1].strip(),  # ID_Objetivo
                        row[2].strip(),  # Importancia
                        row[3].strip() if row[3] else None,  # ID_Prerequisito
                        row[4].strip() if row[4] else None,  # ID_Objetivo_Prerequisito
                    ),
                )
                count2 += 1  # Increment only after successful insertion
            except psycopg2.errors.UniqueViolation as e:
                conn.rollback()
                print(
                    f"Primary Key violation for row {row}: A record with the same combination of "
                    f"(ID, ID_Objetivo, ID_Prerequisito, ID_Objetivo_Prerequisito) already exists. Details: {e}"
                )
                error_count += 1
            except psycopg2.errors.ForeignKeyViolation as e:
                conn.rollback()
                print(
                    f"Foreign Key violation for row {row}: Either ID={row[0]}, ID_Objetivo={row[1]}, "
                    f"ID_Prerequisito={row[3]}, or ID_Objetivo_Prerequisito={row[4]} does not exist in the corresponding table. Details: {e}"
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
    print(f"Data loaded into the RA_Links table from {csv_file}.")
    print(f"Number of rows that could not be added: {error_count}")
    print(f"Total rows processed: {count}")
    print(f"Total rows successfully inserted: {count2}")

# Example usage
csv_file = r"Curricular-Analyst-UA\Análisis_curricular\Database RA_Links\RA_Links.csv"  # Path to your CSV file
load_ra_links_from_csv(csv_file)

# Close the connection
cur.close()
conn.close()
print("Connection closed.")
