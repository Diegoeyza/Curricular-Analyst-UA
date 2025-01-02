README for creator.js
---

Overview
--------
The `creator.js` script automates the extraction, transformation, and insertion of data between Google Sheets. It processes data from a source spreadsheet (`MAESTRO` sheet), filters and maps the data to a required format, and inserts it into a target sheet named `HT` in the active spreadsheet. Additionally, it enriches data by cross-referencing values from a dictionary sheet (`Diccionario`).

Setup Instructions
------------------
1. Open Google Apps Script
   - Navigate to the Google Sheets document where you want to run the script.
   - Click on `Extensions` > `Apps Script`.
   - Copy and paste the `creator.js` script into the script editor.

2. Set Up the Source Spreadsheet
   - Identify the source spreadsheet you want to extract data from.
   - Replace the `sourceSpreadsheetId` value in the script with the unique ID of the source spreadsheet.
     
     Example:
     ```javascript
     const sourceSpreadsheetId = "1o6HftjnQiU4EB1T9mwZ5FntfkZqy9Bj5wkZKbyHl-m0"; // Replace this with your source spreadsheet ID
     ```

3. Verify the Sheet Names
   - Confirm that the source sheet (`MAESTRO`) exists in the source spreadsheet.
   - Ensure a sheet named `Diccionario` exists in the active spreadsheet, as it is used for enriching the data.

4. Run the Script
   - In the script editor, select the `extractAndInsertData` function.
   - Click on the `Run` button to execute the script.

5. Review the Output
   - The script creates (or clears and overwrites) a sheet named `HT` in the active spreadsheet and populates it with the transformed data.

Key Features
------------
- Column Mapping
  - Maps specific columns from the `MAESTRO` sheet to a predefined structure in the `HT` sheet.
  - Logs missing columns for debugging.

- Data Filtering
  - Filters rows where:
    - `"CURSO MANDANTE"` is `"si"` (case insensitive).
    - `"Habilidades Transversales"` is not empty.

- Data Enrichment
  - Matches values in the `"Habilidades Transversales"` column with entries in the `Diccionario` sheet.
  - Populates corresponding `"Significado HT a medir"`, `"Implementación"`, and `"Evaluación de la HT"` columns.

- Formatting
  - Applies formatting to the header row (bold text, text wrapping, adjusted heights and widths).  

How to Get the Source Spreadsheet Link
--------------------------------------
To obtain the link or ID of the source spreadsheet:
1. Open the source spreadsheet in Google Sheets.
2. Copy the URL from the browser's address bar.
   - Example URL:
     `https://docs.google.com/spreadsheets/d/1o6HftjnQiU4EB1T9mwZ5FntfkZqy9Bj5wkZKbyHl-m0/edit`
3. Extract the part after `/d/` and before `/edit`. This is the spreadsheet ID:
   `1o6HftjnQiU4EB1T9mwZ5FntfkZqy9Bj5wkZKbyHl-m0`

Replace the placeholder `sourceSpreadsheetId` in the script with this ID.

Additional Notes
----------------
- **Permissions**: Ensure the script has permission to access both the active and source spreadsheets. You may need to authorize the script on the first run.
- **Error Handling**: The script logs any missing columns or mismatched dictionary values for easier debugging.
- **Customization**: Update the `requiredColumns` or sheet names to match your specific requirements.

--- 

Send Mails
---
Description
-----------
This code can be added to the spreadsheet and allows to send the predefined mail in the HT sheet to all of the mail adresses in the sheet, if they have a predefined mail template