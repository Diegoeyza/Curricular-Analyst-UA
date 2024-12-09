function checkClassAndInsertData() {
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    const ui = SpreadsheetApp.getUi();
  
    // Ask the user for the class name
    const response = ui.prompt("Class Name", "Enter the class name to check:", ui.ButtonSet.OK_CANCEL);
    if (response.getSelectedButton() !== ui.Button.OK) {
      ui.alert("Operation canceled.");
      return;
    }
    const className = response.getResponseText().trim();
    if (!className) {
      ui.alert("Class name cannot be empty.");
      return;
    }
  
    // Get the current sheet and read the first row for column IDs
    const currentSheet = spreadsheet.getActiveSheet();
    const columnHeaders = currentSheet.getRange(1, 4, 1, currentSheet.getLastColumn() - 3).getValues()[0];
  
    // Generate IDs for columns based on their position
    const columnIds = columnHeaders.map((_, index) => `${className}-${index + 1}`);
  
    // Get all data in the sheet starting from the 2nd row
    const dataRange = currentSheet.getRange(2, 1, currentSheet.getLastRow() - 1, currentSheet.getLastColumn());
    const data = dataRange.getValues();
  
    // Get the APE_Courses sheet and ensure it exists
    const apeCoursesSheet = spreadsheet.getSheetByName("APE_Courses");
    if (!apeCoursesSheet) {
      ui.alert("The sheet named 'APE_Courses' does not exist.");
      return;
    }
  
    // Get the general sheet and ensure it exists
    const generalSheet = spreadsheet.getSheetByName("general");
    if (!generalSheet) {
      ui.alert("The sheet named 'general' does not exist.");
      return;
    }
  
    // Fetch data from the general sheet for mapping IDs to second column values
    const generalData = generalSheet.getRange(2, 1, generalSheet.getLastRow() - 1, 2).getValues();
    const generalMap = new Map(generalData.map(row => [row[0], row[1]]));
  
    // Prepare data to insert into APE_Courses
    const entries = [];
  
    data.forEach((row, rowIndex) => {
      const courseId = row[0]; // First column of the row (Course ID)
      for (let colIndex = 3; colIndex < row.length; colIndex++) { // Starting from the 4th column
        if (row[colIndex] === "X") {
          const columnId = columnIds[colIndex - 3];
          const generalDataValue = generalMap.get(courseId) || ""; // Get value from general sheet
          entries.push([columnId, courseId, generalDataValue]);
        }
      }
    });
  
    if (entries.length === 0) {
      ui.alert("No 'X' values found in the current sheet for the selected class.");
      return;
    }
  
    // Sort entries by the numeric value in the first column (ColumnID)
    entries.sort((a, b) => {
      const numA = parseInt(a[0].split("-")[1], 10);
      const numB = parseInt(b[0].split("-")[1], 10);
      return numA - numB;
    });
  
    // Determine the first empty row in APE_Courses
    const lastRow = apeCoursesSheet.getLastRow();
    const startRow = lastRow + 1;
  
    // Insert data into APE_Courses
    apeCoursesSheet.getRange(startRow, 1, entries.length, 3).setValues(entries);
  
    ui.alert(`Successfully inserted ${entries.length} entries into the 'APE_Courses' sheet.`);
  }
  