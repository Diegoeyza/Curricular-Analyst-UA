import pandas as pd
import os

def find(data_find, data_to_find, used, pos):
    for i in range(len(data_find)):
        if ((data_find["name"][i] == data_to_find["TITULO"][pos]) and 
            (i not in used) and 
            (data_find["section"][i] == data_to_find["SECC."][pos]) and 
            (data_find["type"][i][0:3] == data_to_find["TIPO DE REUNIÓN"][pos][0:3])):
            if(data_find["name"][i]=="Fundamentos de Economía"):
                print ("found")
                print(f"{i}:{pos}")
            
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

    # Check if the output file exists
    if os.path.exists(out):
        # Load existing final.csv file if it exists
        df_final = pd.read_csv(out, sep=';', encoding='utf-8')
    else:
        # Create a new DataFrame based on df1 if final.csv doesn't exist
        df_final = df1.copy()

    # Ensure the columns DIA, INICIO, and FIN are of string type
    df_final['DIA'] = df_final['DIA'].astype(str)
    df_final['INICIO'] = df_final['INICIO'].astype(str)
    df_final['FIN'] = df_final['FIN'].astype(str)

    # Fill the DIA, INICIO, FIN columns in df_final using the corresponding data from df2
    for i in range(len(used)):
        df_final.at[used2[i], 'DIA'] = str(df2.at[used[i], 'day'])
        df_final.at[used2[i], 'INICIO'] = str(df2.at[used[i], 'interval_start'])[:-3]
        df_final.at[used2[i], 'FIN'] = str(df2.at[used[i], 'interval_end'])[:-3]

    # Replace NaN values with the string "NULL"
    df_final = df_final.replace({pd.NA: 'NULL', 'nan': 'NULL', None: 'NULL'})

    # Save the final DataFrame back to the CSV file, preserving existing data
    df_final.to_csv(out, sep=';', index=False, encoding='utf-8')

    print(f"Data has been saved to {out}")

combine(r"data_CA\Programación Maestro Macro segunda parte.csv","separated_schedule.csv","final.csv")