Análisis curricular:
1-To begin the analysis download all of the syllabus as pdf and extract them in a specific folder
2-Copy the path of the folder and add it to the pdf_scrapper in the line 127
3-Run the csv_converter to create the tables with the data
4-If you inted to crossreference with another file containing only the valid IDs, convert that file to a csv, put the IDs into a column called CODIGOS and add the file path to the line 4 of the ID_crossreferencer

Horarios_curso:
1-first of all, the file must have a format which is the days of the week from monday to friday and the hours in the 2 rows to the left. The course format should be "ELECTRO (LAB) SEC 1;MARTES;9:30;10:20" where LAB can be replaced with CLAS or AYUD
2- Then use the organizer
3- Then the merger
4- Then the sepparator