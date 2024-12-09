function convertFirstColumnFormat() {
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = spreadsheet.getActiveSheet();
    
    // Get the first column's data, skipping the first row
    const dataRange = sheet.getRange(2, 1, sheet.getLastRow() - 1, 1);
    const data = dataRange.getValues();
  
    // Process each cell to modify its format
    const updatedData = data.map(row => {
      const value = row[0];
      if (typeof value === "string" && value.length > 3) {
        return [value.slice(0, 3) + "_" + value.slice(3)];
      }
      return [value]; // If the value is not in the expected format, keep it as is
    });
  
    // Set the modified data back to the sheet
    dataRange.setValues(updatedData);
  }
  