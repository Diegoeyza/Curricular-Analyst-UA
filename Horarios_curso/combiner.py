import pandas as pd
from datetime import datetime, timedelta

def find(data_find, data_to_find, used, pos):
    for i in range(len(data_find)):
        if ((data_find["name"][i].lower() == data_to_find["TITULO"][pos].lower()) and 
            (i not in used) and 
            (data_find["section"][i] == data_to_find["SECC."][pos]) and 
            (data_find["type"][i] == data_to_find["TIPO DE REUNIÓN"][pos])):
            return i
    return -1

def combine(fill, data, out):
    used = []
    used2 = []
    
    # Load the CSV files
    df1 = pd.read_csv(fill, sep=';')  # file with TITULO, SECC., etc.
    df2 = pd.read_csv(data, sep=';')  # file with name, section, etc.

    # Ensure the column "CUPOS TOTALES" is treated as an integer
    df1['CUPOS TOTALES NRC'] = df1['CUPOS TOTALES NRC'].fillna(0).astype(int)

    # Iterate over df1 to find matches in df2
    for i in range(len(df1["TITULO"])):
        idx = find(df2, df1, used, i)
        if idx != -1:
            used.append(idx)
            used2.append(i)

    # Create a copy of df1 to fill in the data
    df_final = df1.copy()

    # Ensure the columns DIA, INICIO, and FIN are of string type
    df_final['DIA'] = df_final['DIA'].astype(str)
    df_final['INICIO'] = df_final['INICIO'].astype(str)
    df_final['FIN'] = df_final['FIN'].astype(str)

    # Fill the DIA, INICIO, FIN columns in df_final using the corresponding data from df2
    for i in range(len(used)):
        df_final.at[used2[i], 'DIA'] = str(df2.at[used[i], 'day'])
        df_final.at[used2[i], 'INICIO'] = str(df2.at[used[i], 'interval_start'])
        df_final.at[used2[i], 'FIN'] = str(df2.at[used[i], 'interval_end'])

    # Replace NaN values with the string "NULL"
    df_final = df_final.replace({pd.NA: 'NULL', 'nan': 'NULL', None: 'NULL'})

    # Save the final DataFrame to a CSV file with UTF-8 encoding
    df_final.to_csv(out, sep=';', index=False, encoding='utf-8')

# Example usage
combine(r"data_CA\Programación Maestro Macro segunda parte.csv", "separated_schedule.csv", "final.csv")
