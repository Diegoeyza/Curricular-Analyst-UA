function createAndInsertClassData() {
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    const ui = SpreadsheetApp.getUi();
  
    // Ask the user for the class name
    const response = ui.prompt("Class Name", "Enter the class name:", ui.ButtonSet.OK_CANCEL);
    if (response.getSelectedButton() !== ui.Button.OK) {
      ui.alert("Operation canceled.");
      return;
    }
    const className = response.getResponseText().trim();
    if (!className) {
      ui.alert("Class name cannot be empty.");
      return;
    }
  
    // Get the current sheet and read the first row starting from the 4th column
    const currentSheet = spreadsheet.getActiveSheet();
    const dataRow = currentSheet.getRange(1, 4, 1, currentSheet.getLastColumn() - 3).getValues()[0];
  
    // Generate IDs and collect data for insertion
    const ids = [];
    const values = [];
    for (let i = 0; i < dataRow.length; i++) {
      if (dataRow[i]) { // Only process cells with data
        const id = `${className}-${i + 1}`;
        ids.push(id);
        values.push(dataRow[i]);
      }
    }
  
    if (ids.length === 0) {
      ui.alert("No data found in the specified range to generate IDs.");
      return;
    }
  
    // Get the APE sheet and determine the first empty row in column 1
    const apeSheet = spreadsheet.getSheetByName("APE");
    if (!apeSheet) {
      ui.alert("The sheet named 'APE' does not exist.");
      return;
    }
    const lastRow = apeSheet.getLastRow();
    const startRow = lastRow + 1;
  
    // Prepare data for insertion
    const idColumn = ids.map(id => [id]);
    const classColumn = ids.map(() => [className]);
    const valueColumn = values.map(value => [value]);
  
    // Insert data into the APE sheet
    apeSheet.getRange(startRow, 1, ids.length, 1).setValues(idColumn);     // IDs in column 1
    apeSheet.getRange(startRow, 2, ids.length, 1).setValues(classColumn); // Class name in column 2
    apeSheet.getRange(startRow, 3, ids.length, 1).setValues(valueColumn); // Associated values in column 3
  
    ui.alert(`Successfully inserted ${ids.length} entries into the 'APE' sheet.`);
  }
  