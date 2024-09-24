import pandas as pd

# Load the CSV, assuming no header and separating by semicolons
df = pd.read_csv(r'data_CA\horario.csv', header=None, sep=';')

# Select columns for the first section (Lunes to Viernes in the first part)
first_part = df.iloc[:, :7]  # From the first Lunes to the first Viernes (columns 0 to 6)

# Select columns for the second section (Lunes to Viernes in the second part)
second_part = df.iloc[:, 9:16]  # From the second Lunes to the second Viernes (columns 9 to 15)

# Save the first part to a new CSV
first_part.to_csv('first_part.csv', index=False, header=False, sep=';')

# Save the second part to a new CSV
second_part.to_csv('second_part.csv', index=False, header=False, sep=';')

print("CSV files created: first_part.csv and second_part.csv")
