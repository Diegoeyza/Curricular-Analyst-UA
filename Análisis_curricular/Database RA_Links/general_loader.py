import psycopg2
import csv

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    "dbname=links_ra user=postgres password=bduandes host=localhost port=5432"
)
cur = conn.cursor()

# SQL statement to create the Courses table
create_courses_table_sql = """
CREATE TABLE IF NOT EXISTS Courses (
    ID TEXT PRIMARY KEY,
    Nombre TEXT NOT NULL
);
"""

# Create the Courses table
cur.execute(create_courses_table_sql)
conn.commit()
print("Courses table created successfully.")

# Function to load data into the Courses table from a CSV file
def load_courses_from_csv(csv_file):
    with open(csv_file, 'r', encoding='utf-8') as f:  # Open the CSV file
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        for row in reader:
            try:
                # Insert data into the Courses table
                cur.execute(
                    "INSERT INTO Courses (ID, Nombre) VALUES (%s, %s)",
                    (row[0].strip(), row[1].strip()),
                )
            except psycopg2.IntegrityError:
                conn.rollback()
                print(f"Skipping duplicate ID: {row[0]}")
            except Exception as e:
                conn.rollback()
                print(f"Error inserting row {row}: {e}")
    conn.commit()
    print(f"Data loaded into the Courses table from {csv_file}.")

# Example usage
csv_file = r"Curricular-Analyst-UA\Análisis_curricular\Database RA_Links\general.csv"  # Path to your CSV file
load_courses_from_csv(csv_file)

# Close the connection
cur.close()
conn.close()
print("Connection closed.")
