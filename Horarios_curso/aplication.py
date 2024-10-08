from converter import convert_row, process_folder
from xls_separator import extractor

excel_file = r'C:\Users\diego\OneDrive\Documentos\Pythonhw\.vs\Curricular_analyst_UA\data_CA\Calendario Horarios 202420 FORMATO ANTIGUO (16).xlsx'
folder_path = r'extracted_CSV'  # Change this to your folder path
destination=r"data_CA\Programación Maestro Macro segunda parte.csv" #destination file where you want to add the data
extractor(excel_file)
process_folder(folder_path, destination)

convert_row(r"data_CA\Calendario Horarios 202420 FORMATO ANTIGUO (16).xlsx",r"data_CA\Programación Maestro Macro segunda parte.csv")