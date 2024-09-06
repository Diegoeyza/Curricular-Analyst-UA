import PyPDF2
import re
import os

def extract_learning_objectives(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            text += page_text

        # Find the "Objetivos de aprendizaje" section
        start = text.find("ID_OA  Descripción")
        if start != -1:
            # Find where the section ends
            end = text.find("Descripción de Contenidos por Unidad", start)
            if end == -1:
                end = len(text)
            objectives = text[start:end]
            
            # Remove "ID_OA  Descripción"
            objectives = objectives.replace("ID_OA  Descripción", "")
            
            # Replace OA1, OA2, etc., with 1-, 2-, etc., and ensure they are separated by \n
            objectives = re.sub(r'OA(\d+)', r'\1-', objectives)

            # Add newlines before each objective if they don't already exist
            objectives = re.sub(r'(\d+-)', r'\n\1', objectives).strip()

            return objectives
        else:
            return "Section not found."

# Function to extract ID from the file name
def extract_id_from_filename(filename):
    # Use regex to capture the ID (e.g., ICC_5150) from the filename
    match = re.search(r'_\w+_\d+_', filename)
    if match:
        # Strip the leading and trailing underscores
        return match.group().strip('_')
    return None

pdf_path = r"D:\Archivos practica pre prof\202420_ICA_5210_.pdf"  
#D:\Archivos practica pre prof\202420_ICC_3202_.pdf
#D:\Archivos practica pre prof\202420_ICC_5150_.pdf
#D:\Archivos practica pre prof\202420_ICA_5210_.pdf
objectives = extract_learning_objectives(pdf_path)

file_id = extract_id_from_filename(pdf_path)

if file_id:
    output_text = f"ID={file_id}\n" + objectives + "\n\n\n"
else:
    f"ID=missing\n" + objectives + "\n\n\n"

with open("test1.txt", "a", encoding="utf-8") as file:
    file.write(output_text)

file.close
