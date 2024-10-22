// Function to delete existing triggers
function deleteTriggers(triggerName) {
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => {
      if (trigger.getHandlerFunction() === triggerName) {
          ScriptApp.deleteTrigger(trigger);
      }
  });
}

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
  newSheet.getRange(1, 1).setValue("Seleccione un Curso");
  newSheet.getRange(1, 2).setValue("Seleccione un Objetivo de Aprendizaje");
  
  // Set headers for additional dropdowns
  newSheet.getRange(1, 4).setValue("Seleccione Prerrequisito");
  newSheet.getRange(1, 5).setValue("Seleccione el Objetivo de Aprendizaje a enlazar");
  
  // Set header for "Importancia" in column C
  newSheet.getRange(1, 3).setValue("Importancia");

  // Define the importance options
  var importanciaOptions = ["Baja", "Media", "Alta"];
  var importanciaRule = SpreadsheetApp.newDataValidation()
                      .requireValueInList(importanciaOptions)
                      .build();
  newSheet.getRange(2, 3).setDataValidation(importanciaRule); // Set the dropdown for "Importancia" in C2
  
  // Clear previous validation in the learning objective column (B2)
  newSheet.getRange(2, 2).clearDataValidations();
  
  // Set headers for IDs
  newSheet.getRange(4, 1).setValue("ID Curso");
  newSheet.getRange(4, 2).setValue("ID Objetivo");
  newSheet.getRange(4, 3).setValue("Importancia");
  newSheet.getRange(4, 4).setValue("ID Prerrequisito");
  newSheet.getRange(4, 5).setValue("ID Objetivo Prerrequisito");
  
  // Clear any previous IDs
  newSheet.getRange(3, 1, 1, 4).clearContent();
  fit()

  deleteTriggers("updateLearningObjectivesDropdown");

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

          // Get the headers from the first row to determine the correct column indices
          var headers = objectivesSheet.getRange(1, 1, 1, objectivesSheet.getLastColumn()).getValues()[0];

          // Find the column indices for "ID", "ID_Objetivo", and "Objetivo"
          var idColIndex = headers.indexOf("ID") + 1; // +1 because getRange is 1-based index
          var idObjetivoColIndex = headers.indexOf("ID_Objetivo") + 1;
          var objetivoColIndex = headers.indexOf("Objetivo") + 1;

          // Ensure all required columns are found
          if (idColIndex === 0 || idObjetivoColIndex === 0 || objetivoColIndex === 0) {
              Logger.log("Error: One or more columns not found in the 'objectives' sheet.");
              return;
          }

          // Get the learning objectives related to the selected course ID
          var objectivesRange = objectivesSheet.getRange(2, 1, objectivesSheet.getLastRow() - 1, objectivesSheet.getLastColumn()); // Get all rows from row 2 onward
          var objectivesValues = objectivesRange.getValues();
          
          // Filter learning objectives based on the selected course ID
          var filteredObjectives = objectivesValues.filter(function(row) {
              return row[idColIndex - 1] == courseID; // Compare with course ID using the dynamically found index
          }).map(function(row) {
              return row[objetivoColIndex - 1]; // Get the objective using the 'Objetivo' column index
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

      // Get the headers from the first row to determine the correct column indices
      var headers = objectivesSheet.getRange(1, 1, 1, objectivesSheet.getLastColumn()).getValues()[0];

      // Find the column indices for "ID", "ID_Objetivo", and "Objetivo"
      var idColIndex = headers.indexOf("ID") + 1; // +1 because getRange is 1-based index
      var idObjetivoColIndex = headers.indexOf("ID_Objetivo") + 1;
      var objetivoColIndex = headers.indexOf("Objetivo") + 1;

      // Ensure all required columns are found
      if (idColIndex === 0 || idObjetivoColIndex === 0 || objetivoColIndex === 0) {
          Logger.log("Error: One or more columns not found in the 'objectives' sheet.");
          return;
      }

      // Get the learning objectives related to the selected course ID
      var objectivesRange = objectivesSheet.getRange(2, 1, objectivesSheet.getLastRow() - 1, objectivesSheet.getLastColumn()); // Get all rows from row 2 onward
      var objectivesValues = objectivesRange.getValues();

      // Find the corresponding Objective ID for the selected objective
      var objectiveID = null;
      for (var j = 0; j < objectivesValues.length; j++) {
          if (objectivesValues[j][objetivoColIndex - 1] === selectedObjective) { // Compare with objective text in the 'Objetivo' column
              objectiveID = objectivesValues[j][idObjetivoColIndex - 1]; // Get the Objective ID from the 'ID_Objetivo' column
              break;
          }
      }

      // If we found a matching Objective ID
      if (objectiveID) {
          // Set the Objective ID in B3
          sheet.getRange(5, 2).setValue(objectiveID);
      } else {
          // Clear B3 if no matching Objective ID is found
          sheet.getRange(5, 2).clearContent();
      }
  }

  // Check if we are in the "Course Dropdown" sheet and the cell edited is C2 (Importancia)
  if (sheet.getName() === "Course Dropdown" && range.getA1Notation() === "C2") {
      var selectedImportancia = range.getValue(); // Get the selected importancia
      // Set the selected importancia in C5
      sheet.getRange(5, 3).setValue(selectedImportancia); // Set the selected importancia in C5
  }

  // Check if we are in the "Course Dropdown" sheet and the cell edited is A2
  if (sheet.getName() === "Course Dropdown" && range.getA1Notation() === "A2") {
      var selectedCourseID = sheet.getRange(5, 1).getValue(); // Get the Course ID from A5

      // Get the active spreadsheet
      var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
      
      // Get the 'requirements' sheet
      var requirementsSheet = spreadsheet.getSheetByName("requirements");

      // Get the requirement data (ID, Requirement, etc.)
      var requirementsRange = requirementsSheet.getRange(2, 1, requirementsSheet.getLastRow() - 1, 3); // Get ID (col 1), Requirement ID (col 2), Requirement (col 3)
      var requirementsValues = requirementsRange.getValues();
      
      // Filter requirements based on the selected Course ID
      var filteredRequirements = requirementsValues.filter(function(row) {
          return row[0] == selectedCourseID; // Row[0] is the course ID in the 'requirements' sheet
      }).map(function(row) {
          return row[2]; // Get the requirement from column 3 (index 2)
      });

      // If there are requirements for the selected Course ID, add them to dropdown in D2
      if (filteredRequirements.length > 0) {
          var requirementRule = SpreadsheetApp.newDataValidation()
                      .requireValueInList(filteredRequirements)
                      .build();
          sheet.getRange(2, 4).setDataValidation(requirementRule); // Set validation in D2
      } else {
          // If no requirements found, clear validation in D2
          sheet.getRange(2, 4).clearDataValidations();
      }
    
    // Set the first matching Requirement ID in D5
    if (requirementIDs.length > 0) {
      sheet.getRange(5, 4).setValue(requirementIDs[0]); // Set the first matching Requirement ID
    } else {
      sheet.getRange(5, 4).clearContent(); // Clear if no requirements are found
    }
  }

  // Check if we are in the "Course Dropdown" sheet and the cell edited is D2
  if (sheet.getName() === "Course Dropdown" && range.getA1Notation() === "D2") {
    var selectedRequirement = range.getValue(); // Get the selected requirement

    // Get the active spreadsheet
    var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    
    // Get the 'requirements' sheet
    var requirementsSheet = spreadsheet.getSheetByName("requirements");

    // Get the requirement data (ID, Requirement, etc.)
    var requirementsRange = requirementsSheet.getRange(2, 1, requirementsSheet.getLastRow() - 1, 3); // Get ID (col 1), Requirement ID (col 2), Requirement (col 3)
    var requirementsValues = requirementsRange.getValues();
    
    // Find the corresponding Requirement ID for the selected requirement
    var requirementID = null;
    for (var k = 0; k < requirementsValues.length; k++) {
      if (requirementsValues[k][2] === selectedRequirement) { // Compare with requirement text in column 3
        requirementID = requirementsValues[k][1]; // Get the Requirement ID from column 2
        break;
      }
    }

    // If we found a matching Requirement ID
    if (requirementID) {
      // Set the Requirement ID in D5
      sheet.getRange(5, 4).setValue(requirementID);
    }
  }





   // Check if we are in the "Course Dropdown" sheet and the cell edited is D2
if (sheet.getName() === "Course Dropdown" && range.getA1Notation() === "D2") {
  var selectedRequirementID = sheet.getRange(5, 4).getValue(); // Get the Requirement ID from D5

  // Get the active spreadsheet
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  
  // Get the 'objectives' sheet
  var objectivesSheet = spreadsheet.getSheetByName("objectives");

  // Get the learning objectives related to the selected requirement ID
  var objectivesRange = objectivesSheet.getRange(2, 1, objectivesSheet.getLastRow() - 1, 4); // Get Course ID, Objective ID, Objective
  var objectivesValues = objectivesRange.getValues();

  // Filter learning objectives based on the selected Requirement ID
  var filteredObjectivesFromRequirement = objectivesValues.filter(function(row) {
    return row[0] == selectedRequirementID; // Row[0] is the course ID in the 'objectives' sheet
  }).map(function(row) {
    return row[3]; // Get the objective from column 4 (index 3)
  });

  // If there are learning objectives for the selected requirement, apply them as a dropdown to E2
  if (filteredObjectivesFromRequirement.length > 0) {
    var objectiveRule = SpreadsheetApp.newDataValidation()
                    .requireValueInList(filteredObjectivesFromRequirement)
                    .build();
    sheet.getRange(2, 5).setDataValidation(objectiveRule);
  } else {
    // If no objectives are found, clear the validation for E2
    sheet.getRange(2, 5).clearDataValidations();
  }

  // Clear any previous Objective ID in E5 if we are changing the dropdown
  sheet.getRange(5, 5).clearContent();
}

// Update E5 based on the current selection in E2
if (sheet.getName() === "Course Dropdown" && range.getA1Notation() === "E2") {
  var selectedObjective = sheet.getRange(2, 5).getValue(); // Get the selected objective in E2

  // Get the 'objectives' sheet again
  var objectivesSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("objectives");

  // Find the corresponding Objective ID for the selected objective
  var objectivesRange = objectivesSheet.getRange(2, 1, objectivesSheet.getLastRow() - 1, 4);
  var objectivesValues = objectivesRange.getValues();

  var objectiveID = null;
  for (var i = 0; i < objectivesValues.length; i++) {
    if (objectivesValues[i][3] === selectedObjective) { // Compare with objective text in column 4
      objectiveID = objectivesValues[i][1]; // Get the Objective ID from column 2
      break;
    }
  }

  // Set the matching Objective ID in E5
  if (objectiveID !== null) {
    sheet.getRange(5, 5).setValue(objectiveID);
  } else {
    sheet.getRange(5, 5).clearContent(); // Clear if no matching Objective ID is found
  }
}
}