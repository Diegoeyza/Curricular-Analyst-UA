import pandas as pd

# Load the filtered_general.csv file with the relevant IDs
general_df = pd.read_csv('filtered_general.csv', usecols=['ID'])

# Create a set of IDs for quick lookup
valid_ids = set(general_df['ID'])

# Function to filter rows by checking if the ID is in valid_ids
def filter_by_id(chunk):
    return chunk[chunk['ID'].isin(valid_ids)]

# Use chunk processing to handle large files efficiently
chunk_size = 10000  # Adjust the chunk size if needed
filtered_chunks = []

# Load the filtered_requirements.csv file in chunks
for chunk in pd.read_csv('filtered_requirements.csv', chunksize=chunk_size):
    filtered_chunk = filter_by_id(chunk)
    filtered_chunks.append(filtered_chunk)

# Concatenate all filtered chunks
filtered_df = pd.concat(filtered_chunks)

# Save the filtered data to a new CSV file
filtered_df.to_csv('filtered_requirements_filtered.csv', index=False)
