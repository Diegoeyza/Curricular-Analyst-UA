import pandas as pd

# Load the first CSV file containing the ID of the valid courses to cross-reference
df_ids = pd.read_csv('CatálogoPE.csv', sep=';', encoding='utf-8')  # Adjust filename and encoding if needed

# Load the CSV file with the name and ID
df_comparison = pd.read_csv('general.csv', sep=',', encoding='utf-8')  # Adjust filename and encoding if needed

# Check if each ID in the second CSV is present in the CODIGO column of the first CSV
df_comparison['Actual'] = df_comparison['ID'].apply(lambda x: '✓' if x in df_ids['CODIGO'].values else 'X')

# Save the updated DataFrame back to the original CSV file
df_comparison.to_csv('general.csv', index=False, sep=',', encoding='utf-8')

# Create a new DataFrame with only the rows that have '✓' in the 'Actual' column
filtered_df = df_comparison[df_comparison['Actual'] == '✓'][['ID', 'Nombre']]

# Save the filtered DataFrame to a new CSV file
filtered_df.to_csv('filtered_general.csv', index=False, sep=',', encoding='utf-8')

print("Updated CSV 'general.csv' with the cross-references and created 'filtered_general.csv' with valid entries.")
