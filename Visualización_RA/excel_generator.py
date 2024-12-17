import pandas as pd
from sqlalchemy import create_engine, inspect
import psycopg2

def extract_postgres_to_excel(host, database, user, password, output_file):
    """
    Connects to a PostgreSQL database, retrieves all tables with their column headers and data,
    and exports them to an Excel file with each table as a sheet.
    If a table named 'courses' is found, it is saved as 'general' in the Excel file.

    :param host: PostgreSQL host
    :param database: PostgreSQL database name
    :param user: Database username
    :param password: Database password
    :param output_file: Path to save the Excel file
    """
    try:
        # Create PostgreSQL database connection URL
        db_url = f"postgresql+psycopg2://{user}:{password}@{host}/{database}"
        
        # Create database engine
        engine = create_engine(db_url)
        inspector = inspect(engine)

        # Get all table names
        table_names = inspector.get_table_names()
        if not table_names:
            print("No tables found in the database.")
            return

        # Open Excel writer
        with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
            for table_name in table_names:
                # Adjust the sheet name: Rename 'courses' table to 'general'
                sheet_name = "general" if table_name == "courses" else table_name[:31]
                if (sheet_name!="general"):
                    sheet_name = "RA_Links" if table_name == "ra_links" else table_name[:31]

                # Read table into a pandas DataFrame
                query = f'SELECT * FROM "{table_name}"'  # Quoting table name for safety
                df = pd.read_sql(query, engine)

                # Write DataFrame to a sheet
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"Table '{table_name}' exported to sheet '{sheet_name}'.")

        print(f"Data successfully exported to '{output_file}'")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # PostgreSQL credentials
    host = "localhost"
    database = "links_ra"
    user = "postgres"
    password = "bduandes"

    # Output Excel file
    output_file = "postgres_export.xlsx"

    # Run the extraction
    extract_postgres_to_excel(host, database, user, password, output_file)
