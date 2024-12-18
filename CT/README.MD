
# User Guide for Cupos Concentraciones

## Overview
This Excel VBA macro, `casiConcentraciones`, is designed to assign students to specific concentrations based on their preferences, availability of slots, and defined restrictions. If no assignment can be made, the student is marked as "Not Assigned," and their entry is highlighted in red. The macro also includes functions to handle duplicate records.

## Requirements
1. **Input Sheets**:
   - **`Datos`**: This sheet contains student data, including their preferences and relevant details.
   - **`Restricciones`**: This sheet defines the available slots for each concentration in column 8 (starting from row 2).

2. **Output Sheet**:
   - **`Asignaciones`**: This sheet is automatically created by the macro and contains the assignment results.

3. **Columns Expected in `Datos` Sheet**:
   - Column A: Student Name
   - Column B: Email
   - Column C: Student ID (RUT)
   - Column D: Specialty
   - Column F: Concentration Preference
   - Column G: Priority
   - Column J: Academic Priority

## How to Use
1. **Prepare the `Restricciones` Sheet**:
   - List all concentrations in column 1.
   - Enter the number of available slots for each concentration in column 8, starting from row 2.

2. **Prepare the `Datos` Sheet**:
   - Populate the required student information, ensuring all columns mentioned above are filled.

3. **Run the Macro**:
   - Open the VBA editor (Alt + F11).
   - Paste the macro code into a module.
   - Close the VBA editor.
   - In Excel, run the macro from the `Developer` tab or by pressing Alt + F8 and selecting `casiConcentraciones`.

4. **View Results**:
   - The `Asignaciones` sheet will be created with the following columns:
     - **Column A**: Student Name
     - **Column B**: Email
     - **Column C**: Student ID (RUT)
     - **Column D**: Specialty
     - **Column E**: Creation Date (if available)
     - **Column F**: Assigned Concentration
     - **Column G**: Status ("Assigned" or "Not Assigned")
     - **Column H**: Priority
     - **Column I**: Academic Priority
   - Students who could not be assigned are highlighted in red.

## Restrictions Handling
- The macro verifies if a student's specialty is allowed for their preferred concentration based on the restrictions defined in the code.
- If a student cannot be assigned to their preferred concentration due to restrictions or lack of slots, the macro attempts the next available option.

## Duplicate Removal
- After assignments, the macro removes duplicate entries based on the Student ID (RUT).

## Customization
- Modify the concentrations and restrictions by editing the `concentraciones` array and `restricciones` dictionary within the code.
- Adjust column references if the layout of the `Datos` or `Restricciones` sheets changes.

## Error Handling
- If a concentration listed in the `Datos` sheet does not exist in the `Restricciones` sheet, an error message will be displayed.

## Notes
- Save your workbook before running the macro to avoid accidental data loss.
- Ensure that macros are enabled in your Excel application.