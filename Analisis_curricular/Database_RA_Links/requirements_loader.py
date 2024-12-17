import psycopg2
import csv

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    "dbname=links_ra user=postgres password=bduandes host=localhost port=5432"
)
cur = conn.cursor()

# SQL statement to create the requirements table
create_requirements_table_sql = """
CREATE TABLE IF NOT EXISTS requirements (
    ID TEXT NOT NULL,
    ID_Requisito TEXT NOT NULL,
    FOREIGN KEY (ID) REFERENCES Courses(ID),
    FOREIGN KEY (ID_Requisito) REFERENCES Courses(ID),
    PRIMARY KEY (ID, ID_Requisito)
);
"""

# Create the requirements table
cur.execute(create_requirements_table_sql)
conn.commit()
print("requirements table created successfully.")

# Function to load data into the requirements table from a CSV file
def load_requirements_from_csv(csv_file):
    error_count = 0  # Counter for rows that could not be added
    count=0
    count2=0
    with open(csv_file, 'r', encoding='utf-8') as f:  # Open the CSV file
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        for row in reader:
            count+=1
            # Insert data into the requirements table
            cur.execute(
                "INSERT INTO requirements (ID, ID_Requisito) VALUES (%s, %s)",
                (row[0].strip(), row[1].strip()),
                )
    conn.commit()
    print(f"Data loaded into the requirements table from {csv_file}.")
    print(f"Number of rows that could not be added: {error_count}")
    print(count)
    print(count2)

# Example usage
csv_file = r"Curricular-Analyst-UA\Análisis_curricular\Database RA_Links\requirements.csv"  # Path to your CSV file
load_requirements_from_csv(csv_file)

# Close the connection
cur.close()
conn.close()
print("Connection closed.")
