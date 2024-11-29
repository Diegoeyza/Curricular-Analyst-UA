import pandas as pd
import json
from sqlalchemy import create_engine

# Path to the exported data
data_file_path = r"C:\Users\diego\Downloads\part-00000-390000c4-de5b-4fb7-95ca-7923acc4a47d-c000.json"

# Database connection parameters
db_params = {
    'dbname': 'Canvas',
    'user': 'postgres',
    'password': 'bduandes',
    'host': 'localhost',
    'port': 5432  # default PostgreSQL port
}

# Create a connection engine to PostgreSQL
engine = create_engine(f'postgresql://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}:{db_params["port"]}/{db_params["dbname"]}')

# Read the JSON data into a DataFrame
df = pd.read_json(data_file_path, lines=True)

# Check for any dictionary-type columns and convert them to strings
for col in df.columns:
    if df[col].apply(type).eq(dict).any():
        df[col] = df[col].apply(lambda x: json.dumps(x) if isinstance(x, dict) else x)

# Insert data into the PostgreSQL table
table_name = 'submissions'
df.to_sql(table_name, engine, if_exists='replace', index=False)

print(f"Data from '{data_file_path}' has been imported into table '{table_name}'.")
