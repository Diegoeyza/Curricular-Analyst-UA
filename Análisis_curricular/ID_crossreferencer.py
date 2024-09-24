import pandas as pd

# Load the first CSV file containing the ID of the valid courses to cross-reference
df_ids = pd.read_csv('CatálogoPE.csv', sep=';', encoding='utf-8')  # Adjust filename and encoding if needed

# Load the CSV file with the name and ID columns
df_comparison = pd.read_csv('general.csv', sep=',', encoding='utf-8')  # Adjust filename and encoding if needed

# Check if each ID in the second CSV is present in the CODIGO column of the first CSV
df_comparison['Actual'] = df_comparison['ID'].apply(lambda x: '✓' if x in df_ids['CODIGO'].values else 'X')

# Ask the user which filter to apply: 'Actual' or 'Tipo'
filter_choice = input("Choose filter method (1: Actual [default], 2: Tipo): ")

if filter_choice == '2':
        # Load the CSV file that contains only the 'Tipo' column and associate it with the 'ID'
    df_tipo = pd.read_csv('tipo.csv', sep=',', encoding='utf-8')  # Adjust filename and encoding if needed

    # Merge the 'df_comparison' and 'df_tipo' dataframes based on the 'ID' column
    df_comparison = pd.merge(df_comparison, df_tipo[['ID', 'Tipo']], on='ID', how='left')

    # Filter using 'Tipo' column: Remove rows where 'Tipo' is 'A'
    filtered_df = df_comparison[df_comparison['Tipo'] != 'A'][['ID', 'Nombre']]

    # Save the updated DataFrame back to the original CSV file
    df_comparison.to_csv('general.csv', index=False, sep=',', encoding='utf-8')

    # Save the filtered DataFrame to a new CSV file
    filtered_df.to_csv('filtered_general.csv', index=False, sep=',', encoding='utf-8')

    print("Updated 'general.csv' with the cross-references and created 'filtered_general.csv'.")

else:
    # Default filtering: Keep only rows where 'Actual' is '✓'
    filtered_df = df_comparison[df_comparison['Actual'] == '✓'][['ID', 'Nombre']]
    
    # Additionally, create a new DataFrame with the rows where 'Actual' is 'X'
    not_found_df = df_comparison[df_comparison['Actual'] == 'X'][['ID', 'Nombre']]

    # Add a new column 'Tipo' and fill it with 0
    not_found_df['Tipo'] = 0

    # Save the 'X' marked rows with the added 'Tipo' column to a new CSV
    not_found_df.to_csv('tipo.csv', index=False, sep=',', encoding='utf-8')

    # Save the updated DataFrame back to the original CSV file
    df_comparison.to_csv('general.csv', index=False, sep=',', encoding='utf-8')

    # Save the filtered DataFrame to a new CSV file
    filtered_df.to_csv('filtered_general.csv', index=False, sep=',', encoding='utf-8')

    print("Updated 'general.csv' with the cross-references and created 'filtered_general.csv' and 'tipo' which can be modified.")
