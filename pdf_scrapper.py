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

        start = text.find("ID_OA  Descripción")
        if start != -1:
            end = text.find("Descripción de Contenidos por Unidad", start)
            if end == -1:
                end = len(text)
            objectives = text[start:end]
            objectives = objectives.replace("ID_OA  Descripción", "")
            objectives = re.sub(r'OA(\d+)', r'\1-', objectives)
            objectives = re.sub(r'(\d+-)', r'\n\1', objectives).strip()
            return objectives
        else:
            return "Section not found."

def extract_id_from_filename(filename):
    match = re.search(r'_\w+_\d+_', filename)
    if match:
        return match.group().strip('_')
    return None


def process_pdfs_in_folder(folder_path, output_file):
    with open(output_file, "w", encoding="utf-8") as file1:

        for filename in os.listdir(folder_path):

            if filename.endswith(".pdf"):
                pdf_path = os.path.join(folder_path, filename)
                print(f"Processing {filename}...")

                objectives = extract_learning_objectives(pdf_path)

                file_id = extract_id_from_filename(filename)

                if file_id:
                    output_text = f"ID={file_id}\n" + objectives
                else:
                    output_text = objectives

                file1.write(output_text + "\n\n\n")
                print(f"Finished processing {filename}.\n")

# Specify the folder containing the PDFs and the output file
folder_path = r"D:\Archivos practica pre prof"
output_file = "test1.txt"

process_pdfs_in_folder(folder_path, output_file)
