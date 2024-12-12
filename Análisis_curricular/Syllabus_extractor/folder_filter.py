import os
import re

# Define the folder path
folder_path = r"C:\Users\diego\OneDrive\Documentos\Pythonhw\.vs\Curricular_analyst_UA\data"

# Regular expression to capture code and ID based on the updated pattern
file_pattern = re.compile(r'(\d{6})_((?:IC[A-Z]|ING|IOC)_\d+)_NRC_\d+')

# Dictionary to store the latest file for each ID
latest_files = {}

# List to keep track of files that should be deleted
files_to_delete = []

# Iterate through the files in the folder
for filename in os.listdir(folder_path):
    match = file_pattern.match(filename)
    
    if match:
        # Extract the code and ID
        code = match.group(1)
        file_id = match.group(2)
        code_int = int(code)  # Convert code to integer for comparison

        # Check if we already have a file with this ID
        if file_id in latest_files:
            existing_code, existing_filename = latest_files[file_id]

            # Compare the codes
            if code_int > existing_code:
                # If the current file has a newer code, mark the older one for deletion
                files_to_delete.append(existing_filename)
                latest_files[file_id] = (code_int, filename)
            else:
                # Mark the current file for deletion if it's older
                files_to_delete.append(filename)
        else:
            # If this is the first file for the ID, add it to the dictionary
            latest_files[file_id] = (code_int, filename)

# Output the files that will be deleted
print("Files that will be deleted:")
for filename in files_to_delete:
    print(filename)

# Delete the files
for filename in files_to_delete:
    file_path = os.path.join(folder_path, filename)  # Create the full file path
    os.remove(file_path)  # Delete the file
    print(f"Deleted: {file_path}")

# Output the remaining files (the latest ones for each ID)
print("\nRemaining files (latest versions for each ID):")
for file_id, (code, filename) in latest_files.items():
    print(f"File: {filename}, Code: {code}, ID: {file_id}")
