# Database Query Interface

This project provides a graphical user interface (GUI) for executing predefined SQL queries on a PostgreSQL database. It allows users to view query results and download them as formatted Excel files.

## Features
- Connects to a PostgreSQL database using user-specified credentials.
- Provides predefined queries to fetch data from the database.
- Allows filtering query results based on user input.
- Displays results in a scrollable text widget.
- Exports results to an Excel file with formatted headers and cells.

## Prerequisites
Ensure you have the following installed:
1. Python 3.8 or later
2. PostgreSQL database with the necessary tables and data
3. Required Python libraries (see installation section)

## Installation
Install the required Python libraries using pip:
```bash
pip install psycopg2 pandas openpyxl
```

## How to Use

### Step 1: Database Setup
Update the database credentials in the `DB_CREDENTIALS` variable inside the code:
```python
DB_CREDENTIALS = "dbname=your_database user=your_user password=your_password host=your_host port=your_port"
```
Ensure that the database contains the following tables:
- `courses`
- `objectives`
- `requirements`
- `ra_links`

### Step 2: Run the Application
Execute the script to launch the GUI:
```bash
python your_script.py
```

### Step 3: Execute Queries
1. Use the provided buttons to run predefined queries.
2. Optionally, enter a course name or ID in the input box to filter results.
3. Query results will be displayed in the text area below.

### Step 4: Export Results
1. Click the "Download Report as .xlsx" button to export the displayed results to an Excel file.
2. Save the file to your desired location.

## Predefined Queries
1. **Courses Query**: Retrieves course names and IDs.
2. **Objectives Query**: Retrieves objectives and their associated IDs.
3. **Requirements Query**: Retrieves requirements and their IDs.
4. **RA Links Query**: Retrieves RA links with details like prerequisites and objectives.
5. **Number of Unlinked Objectives**: Counts unlinked objectives per course.
6. **Incoming and Outgoing Objective Links**: Retrieves links where a course is either a prerequisite or has prerequisites.

### Adding a New Query
1. Define a new function in the script, similar to existing query functions:
    ```python
    def query_new():
        query = "SELECT column1, column2 FROM table WHERE condition;"
        df = execute_query(query)
        show_results(df)
    ```
2. Add a button in the `create_ui` function to link the new query function:
    ```python
    button_new = Button(root, text="New Query", command=query_new, ...)
    button_new.grid(row=X, column=Y, ...)
    ```

## Notes
- Ensure the database is running and accessible before launching the application.
- The GUI adapts to screen size but is optimized for a resolution of 900x700.
- Results are downloaded in `.xlsx` format, with centered and bold headers.

## Troubleshooting
- **Database Connection Error**: Check your database credentials and network connection.
- **Query Execution Error**: Verify that the SQL query is valid and the database tables exist.
- **No Data to Download**: Ensure a query is executed before downloading the report.

## Author
Kylar
