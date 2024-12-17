function onOpen() {
  // Create a custom menu in the Google Sheets UI
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('Actions')
    .addItem('Agregar', 'copyRowData')
    .addItem("Eliminar última entrada", "deleteLastAddedRow")
    .addItem("Push","copyDataToRALinks")
    .addItem("Eliminar Links","deleteAllAddedRows")
    .addToUi();
}


function copyRowData() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  
  // Read the data from row 5 between columns A and E
  const rowData = sheet.getRange('A5:E5').getValues()[0];
  
  // Find the first empty row starting from row 8
  let targetRow = 8;
  while (sheet.getRange('A' + targetRow).getValue() !== '') {
    targetRow++;
  }
  
  // Write the data to the first empty row found
  sheet.getRange(targetRow, 1, 1, 5).setValues([rowData]);
}

function deleteLastAddedRow() {
  // Get the active spreadsheet and the current sheet
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  
  // Start checking from row 9 and find the last non-empty row
  let lastRow = 9;
  while (sheet.getRange('A' + lastRow).getValue() !== '') {
    lastRow++;
  }
  
  // Move back to the last non-empty row
  lastRow--;
  
  // If there's a valid row to delete, remove it
  if (lastRow >= 9) {
    sheet.deleteRow(lastRow);
  }
}

function deleteAllAddedRows() {
  // Get the active spreadsheet and the current sheet
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  
  // Start checking from row 9 and find the last non-empty row
  let lastRow = 8;
  while (sheet.getRange('A' + lastRow).getValue() !== '') {
    lastRow++;
  }
  while (lastRow!=7){
    sheet.deleteRow(lastRow);
    lastRow--;
  }
}

function copyDataToRALinks() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  
  // Check if the 'RA_Links' sheet exists, if not, create it
  let raLinksSheet = ss.getSheetByName('RA_Links');
  if (!raLinksSheet) {
    raLinksSheet = ss.insertSheet('RA_Links');
    // Set the header row in 'RA_Links'
    const headers = ['ID Curso', 'ID Objetivo', 'Importancia', 'ID Prerrequisito', 'ID Objetivo Prerrequisito'];
    raLinksSheet.getRange('A1:E1').setValues([headers]);
  }
  
  // Get the 'Course Dropdown' sheet
  const courseDropdownSheet = ss.getSheetByName('Course Dropdown');
  if (!courseDropdownSheet) {
    Logger.log('Course Dropdown sheet not found');
    return;
  }
  
  // Read data from 'Course Dropdown' starting from row 8, columns A to E
  const dataRange = courseDropdownSheet.getRange('A9:E' + courseDropdownSheet.getLastRow());
  const data = dataRange.getValues();
  
  // Filter out empty rows
  const filteredData = data.filter(row => row.some(cell => cell !== ''));
  
  // Find the first empty row in 'RA_Links' to start appending data
  const lastRowRA_Links = raLinksSheet.getLastRow();
  const startRow = lastRowRA_Links + 1;
  
  // Append the filtered data to 'RA_Links'
  if (filteredData.length > 0) {
    raLinksSheet.getRange(startRow, 1, filteredData.length, 5).setValues(filteredData);
  }
}
