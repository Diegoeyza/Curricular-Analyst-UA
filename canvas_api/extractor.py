import pandas as pd
import psycopg2
from tqdm import tqdm  # For progress bar

# Database connection parameters
db_params = {
    'dbname': 'Canvas',
    'user': 'postgres',
    'password': 'bduandes',
    'host': 'localhost',
    'port': 5432
}

# Path to the exported data
data_file_path = r"C:\Users\diego\Downloads\part-00000-390000c4-de5b-4fb7-95ca-7923acc4a47d-c000.json"

# Table name in the database
table_name = 'submissions'

# Batch size for inserts
batch_size = 10000

# Connect to the database
conn = psycopg2.connect(
    dbname=db_params['dbname'],
    user=db_params['user'],
    password=db_params['password'],
    host=db_params['host'],
    port=db_params['port']
)
cursor = conn.cursor()

# Read JSON data
print("Loading JSON data...")
df = pd.read_json(data_file_path, lines=True)

# Flatten JSON data if necessary
print("Flattening JSON data...")
# Flatten "key" and "value" dictionaries into separate columns
key_df = pd.json_normalize(df['key'])
value_df = pd.json_normalize(df['value'])
meta_df = pd.json_normalize(df['meta'])

# Merge all columns back into a single DataFrame
df_flattened = pd.concat([key_df, value_df, meta_df], axis=1)

# Replace NaN with None for database compatibility
df_flattened = df_flattened.where(pd.notnull(df_flattened), None)

# Convert numpy data types to native Python types
print("Converting data types...")
df_flattened = df_flattened.applymap(
    lambda x: x.item() if isinstance(x, (pd.Int64Dtype, pd.Float64Dtype, pd.Timestamp)) else x
)

# Get column names for dynamic SQL insertion
columns = ', '.join(df_flattened.columns)
placeholders = ', '.join(['%s'] * len(df_flattened.columns))

# Create the table if it doesn't already exist
print("Creating table...")
create_table_query = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    {', '.join([f"{col} TEXT" for col in df_flattened.columns])}
);
"""
cursor.execute(create_table_query)
conn.commit()

# Insert data in batches with a progress bar
print("Uploading data...")
for i in tqdm(range(0, len(df_flattened), batch_size)):
    batch = df_flattened.iloc[i:i + batch_size]
    records = batch.to_records(index=False)
    values = [tuple(map(lambda x: x.item() if hasattr(x, "item") else x, row)) for row in records]

    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    cursor.executemany(insert_query, values)
    conn.commit()

# Close the database connection
cursor.close()
conn.close()

print("Data upload completed successfully!")
