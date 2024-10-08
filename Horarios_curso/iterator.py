import pandas as pd
import re

df = pd.read_csv("separated_schedule.csv", sep=';')
for i in range (0, len(df["name"])):
    if i>0:
        if df["name"][i]!=df["name"][i-1]:
            print(df["name"][i])
    else:
        print(df["name"][i])

print("-----------")
df_maestro = pd.read_csv(r'data_CA\Programación Maestro Macro segunda parte.csv', sep=';')
df_maestro['CUPOS TOTALES NRC'] = df_maestro['CUPOS TOTALES NRC'].fillna(0).astype(int)
# for i in range (0, len(df_maestro["TITULO"])):
#     if i>0:
#         if df_maestro["TITULO"][i]!=df_maestro["TITULO"][i-1]:
#             print(df_maestro["TITULO"][i])
#     else:
#         print(df_maestro["TITULO"][i])