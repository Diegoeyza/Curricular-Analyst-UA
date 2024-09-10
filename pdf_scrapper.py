import PyPDF2
import re
import os

import PyPDF2
import re
import os

def extract_course_name(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        first_page_text = reader.pages[0].extract_text()
        # Extract the course name by looking for the pattern before " - ICA"
        # Adjusted regex to handle possible leading text and various spacing
        match = re.search(r'^(.+?)\s+- ICA \d+', first_page_text, re.DOTALL)
        if match:
            course_name = match.group(1).strip()
            # Remove newlines and extra spaces
            course_name = re.sub(r'\s+', ' ', course_name)
            return course_name
        return "Course name not found."

def extract_learning_objectives(pdf_path, file_id):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            text += page_text

        start = text.find("ID_OA  Descripción")
        if start != -1:
            end = text.find("Descripción de Contenidos por Unidad", start)
            if end == -1:
                end = len(text)

            # Define the end of the learning objectives section
            objectives = text[start:end]

            # Remove the part that says ID_OA and the following description with an empty space
            objectives = objectives.replace("ID_OA  Descripción", "")

            # Remove any unnecessary newlines
            objectives = re.sub(r'\n+', ' ', objectives)

            # Replace the OA number with the file ID and append the original number at the end with a semicolon and space
            objectives = re.sub(r'OA(\d+)', lambda match: f'{file_id}-{match.group(1)}; ', objectives)

            # Insert a newline before each objective, and remove leading spaces from each objective
            objectives = re.sub(r'(\w+_\d+-\d+;)\s+', r'\n\1', objectives).strip()

            return objectives
        else:
            return "Section not found."

def extract_id_from_filename(filename):
    # Use regular expressions to extract the ID from the filename
    match = re.search(r'_\w+_\d+_', filename)
    if match:
        return match.group().strip('_')
    return None

def process_pdfs_in_folder(folder_path, output_file):
    # Using utf-8 as most of the pdf files are in Spanish and use accents
    with open(output_file, "w", encoding="utf-8") as file1:
        # Go to the beginning of the output (txt) file
        file1.seek(0)
        file1.truncate()

        for filename in os.listdir(folder_path):
            # Extract all of the PDF files from the folder
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(folder_path, filename)
                print(f"Processing {filename}...")

                file_id = extract_id_from_filename(filename)
                
                if not file_id:
                    print(f"Could not extract ID from filename {filename}. Skipping...")
                    continue

                course_name = extract_course_name(pdf_path)
                objectives = extract_learning_objectives(pdf_path, file_id)

                # Format the ID and course name
                output_text = f"ID={file_id}\nNombre={course_name}\n" + objectives

                # Separate each pdf written in the txt
                file1.write(output_text + "\n\n\n")
                print(f"Finished processing {filename}.\n")

# Specify the folder containing the PDFs and the output file
folder_path = r"D:\Test practica"
output_file = "test1.txt"

process_pdfs_in_folder(folder_path, output_file)



#nombre; codigo; id objetivo; descripción objetivo; código prerrequisito; código dependencia
#generar arcos entre prerrequisitos que no son dependencia directa