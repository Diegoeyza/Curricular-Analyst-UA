function markNonMatchingCells() {
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    const currentSheet = spreadsheet.getActiveSheet();
    const generalSheet = spreadsheet.getSheetByName("general");
    
    if (!generalSheet) {
      SpreadsheetApp.getUi().alert("The sheet named 'general' does not exist.");
      return;
    }
  
    // Get the first column of the current sheet (starting from row 2)
    const currentData = currentSheet.getRange(2, 1, currentSheet.getLastRow() - 1, 1).getValues().flat();
    // Get the first column of the 'general' sheet
    const generalData = new Set(generalSheet.getRange(2, 1, generalSheet.getLastRow() - 1, 1).getValues().flat());
  
    const range = currentSheet.getRange(2, 1, currentSheet.getLastRow() - 1, 1);
    const backgrounds = range.getBackgrounds();
  
    // Compare and mark cells
    currentData.forEach((value, index) => {
      if (!generalData.has(value)) {
        backgrounds[index][0] = "#FF0000"; // Red
      } else {
        backgrounds[index][0] = "#FFFFFF"; // Reset to white
      }
    });
  
    range.setBackgrounds(backgrounds);
  }
  
  