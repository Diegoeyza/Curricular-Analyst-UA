import pandas as pd

# Load the first CSV file containing the ID of the valid courses to cross-reference
df_ids = pd.read_csv('CatálogoPE.csv', sep=';', encoding='utf-8')  # Adjust filename and encoding if needed

# Load the CSV file with the name and ID columns
df_comparison = pd.read_csv('general.csv', sep=',', encoding='utf-8')  # Adjust filename and encoding if needed

# Ask the user which filter to apply: 'Actual' or 'Tipo'
filter_choice = input("Choose filter method (1: Actual [default], 2: Tipo): ")

if filter_choice == '2':
    # Filter using 'Actual' column: Remove rows where 'Actual' is 'X'
    filtered_df = df_comparison[df_comparison['Actual'] != 'X'][['ID', 'Nombre']]

    # Save the updated DataFrame back to the original CSV file
    df_comparison.to_csv('general.csv', index=False, sep=',', encoding='utf-8')

    # Now load 'requirements.csv' and remove rows where 'Nombre_requisito' does not exist in 'Nombre' from 'general.csv'
    df_requisitos = pd.read_csv('requirements.csv', sep=',', encoding='utf-8')

    # Filter rows where 'Nombre_Requisito' exists in 'Nombre' of 'general.csv'
    df_requisitos_filtered = df_requisitos[df_requisitos['Nombre_Requisito'].isin(filtered_df['Nombre'])]

    # Save the filtered 'requisitos.csv'
    df_requisitos_filtered.to_csv('filtered_requirements.csv', index=False, sep=',', encoding='utf-8')

    # Now do the same for 'objectives.csv'
    df_objectives = pd.read_csv('objectives.csv', sep=',', encoding='utf-8')

    df_objectives_filtered = df_objectives[df_objectives['ID'].isin(filtered_df['ID'])]
    df_objectives_filtered = pd.merge(df_objectives_filtered, filtered_df[['ID', 'Nombre']], on='ID', how='left')
    df_objectives_filtered.to_csv('filtered_objectives.csv', index=False, sep=',', encoding='utf-8')

    # Save the filtered DataFrame to a new CSV file
    filtered_df.to_csv('filtered_general.csv', index=False, sep=',', encoding='utf-8')

    print("Updated 'general.csv' with the cross-references and created 'filtered_general.csv', 'filtered_requirements.csv' and 'filtered_objectives.csv'.")

else:
    # Check if each ID in the second CSV is present in the CODIGO column of the first CSV
    df_comparison['Actual'] = df_comparison['ID'].apply(lambda x: '✓' if x in df_ids['CODIGO'].values else 'X')

    # Default filtering: Keep only rows where 'Actual' is '✓'
    filtered_df = df_comparison[df_comparison['Actual'] == '✓'][['ID', 'Nombre']]

    # Save the updated DataFrame back to the original CSV file
    df_comparison.to_csv('general.csv', index=False, sep=',', encoding='utf-8')

    # Save the filtered DataFrame to a new CSV file
    filtered_df.to_csv('filtered_general.csv', index=False, sep=',', encoding='utf-8')

    print("Updated 'general.csv' with the cross-references and created 'filtered_general.csv', modify general.csv removing the X if you dont want to remove that course.")
