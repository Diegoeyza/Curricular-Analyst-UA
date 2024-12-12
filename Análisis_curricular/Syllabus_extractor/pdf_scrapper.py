import PyPDF2
import re
import os

def extract_course_name(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        first_page_text = reader.pages[0].extract_text()
        
        # Extract the course name by looking for the pattern before " - ICA"
        match = re.search(r'^(.+?)\s+- \w+ \d+', first_page_text, re.DOTALL)
        if match:
            course_name = match.group(1).strip()
            # Remove newlines and extra spaces
            course_name = re.sub(r'\s+', ' ', course_name)
            return course_name
        return "Course name not found."

def extract_requisitos(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            text += page_text

        # Extract the section starting with "Requisitos / Aprendizajes previos:"
        match = re.search(r'Requisitos / Aprendizajes previos: (.+?)(?:Información de la asignatura|$)', text, re.DOTALL)
        if match:
            requisitos_text = match.group(1).strip()

            # Extract IDs and Names from the requisitos_text
            ids = re.findall(r'\b(IC[A-Z]|ING|IOC)-\n*(\d+)', requisitos_text)
            names = re.findall(r'([A-ZÁÉÍÓÚÑ\s]+?)(?: \((?:IC[A-Z]|ING|IOC)-\n*(?:\d+)\))', requisitos_text)

            # Replace newlines with spaces in names
            names = [name.replace('\n', ' ').strip() for name in names]

            # Replace hyphens with underscores in IDs
            ids = [f"{prefix}_{num}" for prefix, num in ids]
            ids = [id_.replace('-', '_') for id_ in ids]

            # Format the IDs and Names
            ids_str = '; '.join(ids)
            names_str = '; '.join(names)

            return ids_str, names_str
        return "IDs not found", "Names not found"


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
                requisitos_ids, requisitos_names = extract_requisitos(pdf_path)

                # Format the ID and course name
                output_text = (
                    f"ID={file_id}\n"
                    f"Nombre={course_name}\n"
                    f"{objectives}\n"
                    f"ID Requisitos: {requisitos_ids}\n"
                    f"Nombre Requisitos: {requisitos_names}"
                )

                # Separate each PDF written in the txt
                file1.write(output_text + "\n\n\n")
                print(f"Finished processing {filename}.\n")

# Specify the folder containing the PDFs and the output file
folder_path = r"C:\Users\diego\OneDrive\Documentos\Pythonhw\.vs\Curricular_analyst_UA\data"
output_file = "Extracted_text.txt"

process_pdfs_in_folder(folder_path, output_file)




#nombre; codigo; id objetivo; descripción objetivo; código prerrequisito; código dependencia
#generar arcos entre prerrequisitos que no son dependencia directa