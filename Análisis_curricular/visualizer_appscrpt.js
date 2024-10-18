function createDropdownSheet() {
    var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    
    // Check if the "Course Dropdown" sheet already exists
    var existingSheet = spreadsheet.getSheetByName("Course Dropdown");
    if (existingSheet) {
      spreadsheet.deleteSheet(existingSheet);
    }
  
    // Get the 'general' sheet
    var generalSheet = spreadsheet.getSheetByName("general");
  
    // Get the range for the column 'Name' and 'ID' in 'general' sheet (column 1 = ID, column 2 = Name)
    var idRange = generalSheet.getRange(2, 1, generalSheet.getLastRow() - 1, 1);   // IDs (column 1)
    var nameRange = generalSheet.getRange(2, 2, generalSheet.getLastRow() - 1, 1); // Names (column 2)
    var courseNames = nameRange.getValues().flat();
    var courseIDs = idRange.getValues().flat();
  
    // Create a new sheet for the dropdowns
    var newSheet = spreadsheet.insertSheet("Course Dropdown");
  
    // Add dropdown for course names in column A
    var courseRule = SpreadsheetApp.newDataValidation()
                 .requireValueInList(courseNames)
                 .build();
    newSheet.getRange(2, 1).setDataValidation(courseRule); 
  
    // Set headers for both columns
    newSheet.getRange(1, 1).setValue("Select a Course");
    newSheet.getRange(1, 2).setValue("Select Learning Objective");
    
    // Set headers for the additional dropdowns
    newSheet.getRange(1, 4).setValue("Select Additional Objective");
    
    // Clear previous validation in the learning objective column (B2)
    newSheet.getRange(2, 2).clearDataValidations();
    
    // Set headers for IDs
    newSheet.getRange(4, 1).setValue("Course ID");
    newSheet.getRange(4, 2).setValue("Objective ID");
    newSheet.getRange(4, 4).setValue("Additional Objective ID");
    
    // Clear any previous IDs
    newSheet.getRange(3, 1, 1, 3).clearContent();
  
    // Set an onEdit trigger for dynamic updating of the second dropdown
    ScriptApp.newTrigger("updateLearningObjectivesDropdown")
             .forSpreadsheet(spreadsheet)
             .onEdit()
             .create();
  }
  
  function updateLearningObjectivesDropdown(e) {
    var range = e.range;
    var sheet = range.getSheet();
    
    // Check if we are in the "Course Dropdown" sheet and the cell edited is A2
    if (sheet.getName() === "Course Dropdown" && range.getA1Notation() === "A2") {
      var selectedCourse = range.getValue(); // Get the selected course name
      
      // Get the active spreadsheet
      var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
      
      // Get the 'general' sheet
      var generalSheet = spreadsheet.getSheetByName("general");
      
      // Get course names and IDs from the 'general' sheet
      var idRange = generalSheet.getRange(2, 1, generalSheet.getLastRow() - 1, 1);   // IDs (column 1)
      var nameRange = generalSheet.getRange(2, 2, generalSheet.getLastRow() - 1, 1); // Names (column 2)
      var courseNames = nameRange.getValues().flat();
      var courseIDs = idRange.getValues().flat();
      
      // Find the corresponding course ID for the selected course name
      var courseID = null;
      for (var i = 0; i < courseNames.length; i++) {
        if (courseNames[i] === selectedCourse) {
          courseID = courseIDs[i];
          break;
        }
      }
  
      // If we found a matching course ID
      if (courseID) {
        // Get the 'objectives' sheet
        var objectivesSheet = spreadsheet.getSheetByName("objectives");
  
        // Get the learning objectives related to the selected course ID
        var objectivesRange = objectivesSheet.getRange(2, 1, objectivesSheet.getLastRow() - 1, 4); // Get Course ID, Objective ID, Objective
        var objectivesValues = objectivesRange.getValues();
        
        // Filter learning objectives based on the selected course ID
        var filteredObjectives = objectivesValues.filter(function(row) {
          return row[0] == courseID; // Row[0] is the course ID in the 'objectives' sheet
        }).map(function(row) {
          return row[3]; // Get the objective from column 4 (index 3)
        });
  
        // Get the "Course Dropdown" sheet
        var dropdownSheet = spreadsheet.getSheetByName("Course Dropdown");
  
        // If there are learning objectives for the selected course, apply them as a dropdown to B2
        if (filteredObjectives.length > 0) {
          var objectiveRule = SpreadsheetApp.newDataValidation()
                        .requireValueInList(filteredObjectives)
                        .build();
          dropdownSheet.getRange(2, 2).setDataValidation(objectiveRule);
        } else {
          // If no objectives are found, clear the validation for B2
          dropdownSheet.getRange(2, 2).clearDataValidations();
        }
        
        // Set the Course ID in A3
        dropdownSheet.getRange(5, 1).setValue(courseID);
      }
    }
  
    // Check if we are in the "Course Dropdown" sheet and the cell edited is B2
    if (sheet.getName() === "Course Dropdown" && range.getA1Notation() === "B2") {
      var selectedObjective = range.getValue(); // Get the selected objective
  
      // Get the active spreadsheet
      var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
      
      // Get the 'objectives' sheet
      var objectivesSheet = spreadsheet.getSheetByName("objectives");
  
      // Get the learning objectives related to the selected course ID
      var objectivesRange = objectivesSheet.getRange(2, 1, objectivesSheet.getLastRow() - 1, 4); // Get Course ID, Objective ID, Objective
      var objectivesValues = objectivesRange.getValues();
      
      // Find the corresponding Objective ID for the selected objective
      var objectiveID = null;
      for (var j = 0; j < objectivesValues.length; j++) {
        if (objectivesValues[j][3] === selectedObjective) { // Compare with objective text in column 4
          objectiveID = objectivesValues[j][1]; // Get the Objective ID from column 2
          break;
        }
      }
  
      // If we found a matching Objective ID
      if (objectiveID) {
        // Set the Objective ID in B3
        sheet.getRange(5, 2).setValue(objectiveID);
      }
    }
  
    // Check if we are in the "Course Dropdown" sheet and the cell edited is D2
    if (sheet.getName() === "Course Dropdown" && range.getA1Notation() === "D2") {
      var selectedAdditionalObjective = range.getValue(); // Get the selected additional objective
  
      // Get the active spreadsheet
      var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
      
      // Get the 'objectives' sheet
      var objectivesSheet = spreadsheet.getSheetByName("objectives");
  
      // Get the learning objectives related to the selected objective
      var objectivesRange = objectivesSheet.getRange(2, 1, objectivesSheet.getLastRow() - 1, 4); // Get Course ID, Objective ID, Objective
      var objectivesValues = objectivesRange.getValues();
      
      // Find the corresponding additional Objective ID for the selected additional objective
      var additionalObjectiveID = null;
      for (var k = 0; k < objectivesValues.length; k++) {
        if (objectivesValues[k][3] === selectedAdditionalObjective) { // Compare with objective text in column 4
          additionalObjectiveID = objectivesValues[k][1]; // Get the Objective ID from column 2
          break;
        }
      }
  
      // If we found a matching additional Objective ID
      if (additionalObjectiveID) {
        // Set the Additional Objective ID in E3
        sheet.getRange(5, 4).setValue(additionalObjectiveID);
      }
    }
  }
  