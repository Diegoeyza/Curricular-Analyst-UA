function compareAndCreateSheets() {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const raLinksSheet = ss.getSheetByName("RA_Links");
    const generalSheet = ss.getSheetByName("general");
  
    // Check if sheets exist
    if (!raLinksSheet || !generalSheet) {
      throw new Error("Sheets 'RA_Links' or 'general' not found.");
    }
  
    // Get data from the sheets
    const raLinksData = raLinksSheet.getRange(2, 1, raLinksSheet.getLastRow() - 1, 1).getValues().flat();
    const generalData = generalSheet.getRange(2, 1, generalSheet.getLastRow() - 1, 2).getValues();
  
    // Create sets for easy comparison
    const raLinksSet = new Set(raLinksData);
  
    const completedData = [];
    const leftData = [];
  
    // Compare and populate completed and left
    generalData.forEach(([id, name]) => {
      if (raLinksSet.has(id)) {
        completedData.push([id, name]);
      } else {
        leftData.push([id, name]);
      }
    });
  
    // Helper function to create or clear a sheet
    function createOrClearSheet(sheetName) {
      let sheet = ss.getSheetByName(sheetName);
      if (sheet) {
        ss.deleteSheet(sheet);
      }
      sheet = ss.insertSheet(sheetName);
      return sheet;
    }
  
    // Create or clear the "completed" sheet
    const completedSheet = createOrClearSheet("completed");
    if (completedData.length > 0) {
      completedSheet.getRange(1, 1, 1, 2).setValues([["ID", "Name"]]); // Header
      completedSheet.getRange(2, 1, completedData.length, 2).setValues(completedData);
    }
  
    // Create or clear the "Left" sheet
    const leftSheet = createOrClearSheet("Left");
    if (leftData.length > 0) {
      leftSheet.getRange(1, 1, 1, 2).setValues([["ID", "Name"]]); // Header
      leftSheet.getRange(2, 1, leftData.length, 2).setValues(leftData);
    }
  }
  