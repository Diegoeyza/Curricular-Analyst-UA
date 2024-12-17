
# Google Apps Script Project Documentation

This project provides functionality for managing a **Google Sheets-based system** that supports courses, learning objectives, prerequisites, and related dropdown menus. The scripts allow for dynamic interaction, validation, and customization of data within the spreadsheet.

---

## Files and Functions

### **Interface.gs**

This file manages the dynamic generation and updates of dropdown menus and interactions between sheets.

- **deleteTriggers(triggerName)**
  - Deletes existing triggers with a specified handler function name.
  - Ensures no redundant triggers interfere with the spreadsheet's functionality.

- **createDropdownSheet()**
  - Creates a new sheet named **"Course Dropdown"** and populates it with dropdown menus based on data in other sheets.
  - Validates inputs such as course names, learning objectives, prerequisites, and their IDs.
  - Sets up headers for dropdown columns and dynamically updates dropdowns based on user interactions.
  - Automatically deletes any previous **"Course Dropdown"** sheet and recreates it.

- **updateLearningObjectivesDropdown(e)**
  - Updates dropdown menus dynamically based on user selections.
  - Handles interactions in the **"Course Dropdown"** sheet:
    - **Column A (Courses)**: Updates objectives based on the selected course.
    - **Column B (Learning Objectives)**: Displays objectives' corresponding IDs.
    - **Column C (Importance)**: Saves the importance level of a learning objective.
    - **Column D (Prerequisites)**: Filters prerequisites based on the selected course.
    - **Column E (Prerequisite Objectives)**: Displays objectives associated with prerequisites.

---

### **style.gs**

Handles the styling of the "Course Dropdown" sheet for better readability and usability.

- **fit()**
  - Adjusts column widths and row heights for key sections of the **"Course Dropdown"** sheet.
  - Ensures proper alignment and text wrapping for header rows and dropdowns.

---

### **menu.gs**

Defines a custom menu in Google Sheets for additional user actions.

- **onOpen()**
  - Adds a custom menu named **"Actions"** to the Google Sheets interface with the following options:
    - **Agregar**: Copies data from a predefined range to the next available row.
    - **Eliminar última entrada**: Deletes the most recently added data row.
    - **Push**: Copies data to the **"RA_Links"** sheet (detailed in `copyDataToRALinks()`).
    - **Eliminar Links**: Removes all rows added through the system.

- **copyRowData()**
  - Copies data from row 5 (Columns A-E) of the active sheet and appends it to the first empty row starting from row 8.

- **deleteLastAddedRow()**
  - Deletes the last row with data starting from row 9 in the active sheet.

- **deleteAllAddedRows()**
  - Clears all rows added to the sheet from row 9 onwards.

- **copyDataToRALinks()**
  - Copies specific data to a separate sheet named **"RA_Links"**. If the sheet doesn't exist, it creates it and initializes the header row.

---

## Usage

1. Open the **Google Sheet**.
2. A custom menu (**"Actions"**) will appear after the script runs.
3. Use the options in the **"Actions"** menu to manage data efficiently:
   - Add or remove entries.
   - Dynamically populate dropdowns.
   - Ensure the data relationships (courses, objectives, prerequisites) are maintained.

4. To set up the system:
   - Run the `createDropdownSheet()` function from the script editor.
   - The sheet **"Course Dropdown"** will be created with interactive dropdowns for courses, objectives, prerequisites, and importance.

5. Make selections in the **"Course Dropdown"** sheet:
   - Choose a course to see its objectives and prerequisites.
   - Add or delete rows using the menu commands.

---

This project provides a dynamic and user-friendly interface for managing course-related data within **Google Sheets**, improving efficiency and accuracy in data handling.
