import psycopg2
import pandas as pd
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

# Database credentials
DB_CREDENTIALS = "dbname=links_ra user=postgres password=bduandes host=localhost port=5432"

# Establish connection to the database
def connect_db():
    try:
        connection = psycopg2.connect(DB_CREDENTIALS)
        return connection
    except Exception as e:
        messagebox.showerror("Database Connection Error", f"Error connecting to the database: {e}")
        return None

# Function to execute queries
def execute_query(query):
    connection = connect_db()
    if not connection:
        return
    
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]  # Get column names
        df = pd.DataFrame(result, columns=columns)  # Convert result to pandas DataFrame
        connection.commit()
        return df
    except Exception as e:
        messagebox.showerror("Query Execution Error", f"Error executing query: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

# Function to display results in the UI
def show_results(df):
    if df is not None and not df.empty:
        result_text.delete(1.0, END)  # Clear previous results
        result_text.insert(END, df.to_string(index=False))  # Display the DataFrame as text
        global current_df
        current_df = df  # Store the DataFrame for later download
    else:
        messagebox.showinfo("No Results", "No results found or an error occurred.")

# Function to download the report as an xlsx file
def download_report():
    if 'current_df' in globals() and current_df is not None:
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            current_df.to_excel(file_path, index=False)
            messagebox.showinfo("Download Complete", f"Report has been downloaded to {file_path}")
    else:
        messagebox.showwarning("No Data", "No data available to download. Please execute a query first.")

# Function for each predefined query
def query_1():
    query = """
    SELECT nombre, id FROM courses;
    """
    df = execute_query(query)
    show_results(df)

def query_2():
    query = """
    SELECT nombre, id_objetivo, objetivo FROM objectives;
    """
    df = execute_query(query)
    show_results(df)

def query_3():
    query = """
    SELECT r.id, r.id_requisito FROM requirements r;
    """
    df = execute_query(query)
    show_results(df)

# Function to filter query_4 by course name (c.nombre) or course id (c.id)
def query_4():
    course_input = course_input_var.get().strip()  # Get the input from the text box
    
    base_query = """
    SELECT 
        c.nombre AS curso,
        o.objetivo AS objetivo,
        ro.nombre AS prerequisito,
        oo.objetivo AS objetivo_prerequisito,
        rl.importancia
    FROM 
        ra_links rl
    JOIN 
        courses c ON rl.id = c.id
    JOIN 
        objectives o ON rl.id_objetivo = o.id_objetivo
    JOIN 
        courses ro ON rl.id_prerequisito = ro.id
    JOIN 
        objectives oo ON rl.id_objetivo_prerequisito = oo.id_objetivo
    """
    
    # Add filtering condition if the user has provided input for course name or ID
    if course_input:
        if course_input.isdigit():
            # If the input is a number, filter by course ID (c.id)
            query = f"{base_query} WHERE c.id = {course_input}"
        else:
            # Otherwise, filter by course name (c.nombre)
            query = f"{base_query} WHERE c.nombre ILIKE '%{course_input}%'"
    else:
        query = base_query  # If no input, don't apply any filtering

    df = execute_query(query)
    show_results(df)

# Set up the tkinter interface
def create_ui():
    root = Tk()
    root.title("Database Query Interface")
    root.geometry("800x600")  # Increased window size for more space

    # Create a label
    label = Label(root, text="Select a predefined query to execute:", font=("Arial", 16))
    label.grid(row=0, column=0, columnspan=2, pady=10)

    # Create buttons for each query with better styling
    button1 = Button(root, text="Courses Query", command=query_1, width=25, height=2, font=("Arial", 12), relief="solid")
    button1.grid(row=1, column=0, padx=10, pady=10)

    button2 = Button(root, text="Objectives Query", command=query_2, width=25, height=2, font=("Arial", 12), relief="solid")
    button2.grid(row=1, column=1, padx=10, pady=10)

    button3 = Button(root, text="Requirements Query", command=query_3, width=25, height=2, font=("Arial", 12), relief="solid")
    button3.grid(row=2, column=0, padx=10, pady=10)

    button4 = Button(root, text="RA Links Query", command=query_4, width=25, height=2, font=("Arial", 12), relief="solid")
    button4.grid(row=2, column=1, padx=10, pady=10)

    # Entry field for user input (course name or ID)
    global course_input_var
    course_input_var = StringVar()
    entry_label = Label(root, text="Enter Course Name or ID (optional):", font=("Arial", 12))
    entry_label.grid(row=3, column=0, pady=10, padx=10)
    course_input = Entry(root, textvariable=course_input_var, font=("Arial", 12), width=30)
    course_input.grid(row=3, column=1, pady=10, padx=10)

    # Download button
    download_button = Button(root, text="Download Report as .xlsx", command=download_report, width=30, height=2, font=("Arial", 12), relief="solid")
    download_button.grid(row=4, column=0, columnspan=2, pady=10)

    # Text widget to show query results with scroll bar
    result_frame = Frame(root)
    result_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    # Scrollbar for results
    scrollbar = Scrollbar(result_frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    global result_text
    result_text = Text(result_frame, wrap=WORD, height=15, width=90)
    result_text.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.config(command=result_text.yview)
    result_text.config(yscrollcommand=scrollbar.set)

    root.mainloop()

# Run the UI
if __name__ == "__main__":
    current_df = None  # To store the current DataFrame for download
    create_ui()
