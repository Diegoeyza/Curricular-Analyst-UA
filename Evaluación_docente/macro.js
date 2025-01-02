function filterAndCopyByType() {
    // Get the active spreadsheet and its name
    var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    var spreadsheetName = spreadsheet.getName();
    
    // Get the range for UniqueID and Area Type columns
    var rawDataSheet = spreadsheet.getSheetByName("RawData");
    if (!rawDataSheet) {
      SpreadsheetApp.getUi().alert("Sheet 'RawData' not found.");
      return;
    }
    
    var lastRow = rawDataSheet.getLastRow();
    if (lastRow < 2) {
      SpreadsheetApp.getUi().alert("No data found in the 'RawData' sheet.");
      return;
    }
    
    var uniqueIdRange = rawDataSheet.getRange(1, 3, lastRow, 1); // Column C, including row 1
    var areaTypeRange = rawDataSheet.getRange(1, 33, lastRow, 1); // Column AG, including row 1
    
    var uniqueIds = uniqueIdRange.getValues();
    var areaTypes = areaTypeRange.getValues();
    
    // Create a dictionary for UniqueID-to-Type mapping
    var idTypeMap = {};
    for (var i = 0; i < uniqueIds.length; i++) {
      if (uniqueIds[i][0] && areaTypes[i][0]) {
        idTypeMap[uniqueIds[i][0]] = areaTypes[i][0];
      }
    }
    
    // Collect unique types
    var uniqueTypes = new Set(Object.values(idTypeMap));
    
    // Create a prompt for user to select a type
    var typeList = Array.from(uniqueTypes).join("\n");
    var selectedType = SpreadsheetApp.getUi()
      .prompt("Select a type", "Enter a type from the following list:\n" + typeList, SpreadsheetApp.getUi().ButtonSet.OK_CANCEL)
      .getResponseText();
    
    if (!selectedType) {
      SpreadsheetApp.getUi().alert("No type selected. Exiting script.");
      return;
    }
    
    // Create a new spreadsheet
    var newSpreadsheet = SpreadsheetApp.create(spreadsheetName + " - " + selectedType);
    
    // Delete the default sheet created in the new spreadsheet
    var defaultSheet = newSpreadsheet.getSheets()[0];
    
    // Copy each sheet and filter rows based on the selected type
    spreadsheet.getSheets().forEach(function (sheet) {
      if (sheet.getName() !== "RawData" && !["P1 ASIGNATURA ABIERTA", "P5 ASIGNATURA ABIERTA", "P1. PROFESOR ABIERTA", 
                                             "P2. PROFESOR ABIERTA", "P3. PROFESOR ABIERTA", " Aspectos Positivos Profesor ", 
                                             "Mejoras Profesor", "QuestionMapper", "P5 ASIGNATURA ABIERTA"].includes(sheet.getName())) {
        // Get data from the current sheet
        var data = sheet.getDataRange().getValues();
        
        // Find the UniqueID column and row
        var uniqueIdCol = -1;
        var uniqueIdRow = -1;
        for (var row = 0; row < 5; row++) { // Iterate through rows 1 to 5
          for (var col = 0; col < data[0].length; col++) { // Iterate through all columns
            if (data[row][col] === "UniqueID") {
              uniqueIdCol = col;
              uniqueIdRow = row;
              break; // Break the inner loop if found
            }
          }
          if (uniqueIdCol !== -1) {
            break; // Break the outer loop if the column is found
          }
        }
        
        if (uniqueIdCol === -1) {
          return; // Skip if UniqueID column is not found
        }
        
        // Filter rows based on the selected type
        var filteredData = [];
        for (var row = 0; row < data.length; row++) {
          if (row <= uniqueIdRow || (data[row][uniqueIdCol] && idTypeMap[data[row][uniqueIdCol]] === selectedType)) {
            filteredData.push(data[row]);
          }
        }
        
        // Add the filtered data to the new spreadsheet
        if (filteredData.length > 1) { // Ensure there is data to add (beyond the header)
          var newSheet = newSpreadsheet.insertSheet(sheet.getName());
          newSheet.getRange(1, 1, filteredData.length, filteredData[0].length).setValues(filteredData);
        }
      }
    });
    newSpreadsheet.deleteSheet(defaultSheet);
    
    SpreadsheetApp.getUi().alert("Filtering complete! New spreadsheet created: " + newSpreadsheet.getUrl());
  }
  