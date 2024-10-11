from converter import convert_row, process_folder, delete_files
from xls_separator import extractor

#Add the path to the excel file with the timetables
excel_file = r'C:\Users\diego\OneDrive\Documentos\Pythonhw\.vs\Curricular_analyst_UA\data_CA\Calendario Horarios 202420 FORMATO ANTIGUO (16).xlsx'

#There is no need to modify this line, it only defines where the data to be processed will be saved
folder_path = r'extracted_CSV'

#destination file where you want to add the timetables (should be the DPSI)
destination=r"data_CA\Programación Maestro Macro segunda parte.csv"

#Make sure that there is a clean start
delete_files(["Missing_pairs.txt", "Programación Maestro final.xlsx"])

#Process the files
extractor(excel_file)
process_folder(folder_path, destination)

print(f"\n----------------------------------------------------------------------------------------------------------------------------\nThe output file is Programación Maestro final.csv \nThe pairs that could not be matched in the excel file are marked in red, and the ones that could not be matched from the timetable are in Missing_pairs.txt")