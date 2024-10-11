Análisis curricular:

1-To begin the analysis download all of the syllabus as pdf and extract them in a specific folder

2-Copy the path of the folder and add it to the pdf_scrapper in the line 127

3-Run the csv_converter to create the tables with the data

4-If you inted to crossreference with another file containing only the valid IDs, convert that file to a csv, put the IDs into a column called CODIGOS and add the file path to the line 4 of the ID_crossreferencer, the code from the crossreferencer gives the user 2 choices, first choose the option one, that will create a csv file with the name type, which the user can modify replacing the 0 with an A if it is an old course so that it creates a new table that does not include the old courses

Horarios_curso:
1-first of all, the file must have a format which is the days of the week from monday to friday and the hours in the 2 rows to the left. The course format should be "ELECTRO (LAB) SEC 1;MARTES;9:30;10:20" where LAB can be replaced with CLAS or AYUD. The course name must not contain commas, the type (CLAS) for example, should always have a space between it and the name, like ELECTRO (CLAS), invalidad cases would be ELECTRO(CLAS) or ELECTRO ( CLAS)


2- Then add the file path from your excel file (the one with the timetables and days of the week) to the [line 5 of the main.py](https://github.com/Diegoeyza/Curricular-Analyst-UA/blob/a79c77a4c8fcb8e9cb2623926d34b067f64dffac/Horarios_curso/main.py#L5) file.


3- Convert your "Programación maestro macro" excel file to a csv (only the sheet with the DPSI) and copy and paste its path to the [line 9 in main.py](https://github.com/Diegoeyza/Curricular-Analyst-UA/blob/a79c77a4c8fcb8e9cb2623926d34b067f64dffac/Horarios_curso/main.py#L9)

4- Now you can run the code in [main.py](Horarios_curso/main.py), it will create 2 output files: 
  I) Programación Maestro final.csv -> This file has the updated programation fro the courses with the timetables, if a row doesn´t have a timetable assigned, it will be marked with red
  II) Missing_pairs.txt -> This file has the timetables that didnt find a match to its corresponding course in Programación Maestro final, with all of their corresponding information


Not admitted formats:
SIMULACION (LAB) SEC 1 (LAB ), should be: SIMULACION (LAB) SEC 1
SIMULACION (LAB) SEC1, should be: SIMULACION (LAB) SEC 1
