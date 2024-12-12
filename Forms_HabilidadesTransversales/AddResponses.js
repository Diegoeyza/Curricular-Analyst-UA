function onOpen() {
    const ui = SpreadsheetApp.getUi();
    ui.createMenu('Actions')
      .addItem('Update Data from Responses', 'updateDataFromResponses')
      .addToUi();
  }
  
  function updateDataFromResponses() {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const responsesSheet = ss.getSheetByName('Responses');
    const firstSheet = ss.getSheets()[0]; // Get the first sheet
    
    const responsesData = responsesSheet.getDataRange().getValues(); // Get all data from the Responses sheet
    const firstSheetData = firstSheet.getDataRange().getValues(); // Get all data from the first sheet
    
    // Find the indexes of the columns in the first sheet
    const firstSheetHeaders = firstSheetData[0];
    const llaveIndexFirstSheet = firstSheetHeaders.indexOf('LLAVE');
    const instrumentoIndexFirstSheet = firstSheetHeaders.indexOf('Instrumento');
    const soloGrupoIndexFirstSheet = firstSheetHeaders.indexOf('¿Evaluará de manera individual o grupal?');
    const vecesEvaluacionIndexFirstSheet = firstSheetHeaders.indexOf('¿Cuántas veces durante el semestre se evalúa la HT?');
    const mesesEvaluacionIndexFirstSheet = firstSheetHeaders.indexOf('¿En qué mes va a evaluar la HT?');
    
    // Create an object to store the latest values from Responses (to handle duplicate LLAVE)
    const latestResponses = {};
  
    // Process each row in Responses sheet
    for (let i = 1; i < responsesData.length; i++) {
      const response = responsesData[i];
      const llave = response[responsesSheet.getRange(1, 1).getColumn() - 1]; // LLAVE is in the first column
      const instrumento = response[responsesSheet.getRange(1, 7).getColumn() - 1]; // Instrumento
      const soloGrupo = response[responsesSheet.getRange(1, 8).getColumn() - 1]; // Solo o en grupo
      const vecesEvaluacion = response[responsesSheet.getRange(1, 9).getColumn() - 1]; // ¿Cuántas veces durante el semestre se evalúa la HT?
      const mesesEvaluacion = response[responsesSheet.getRange(1, 10).getColumn() - 1]; // ¿En qué meses se evalúa la HT?
  
      // Save the latest row (with the last occurrence of LLAVE)
      latestResponses[llave] = {
        instrumento,
        soloGrupo,
        vecesEvaluacion,
        mesesEvaluacion
      };
    }
    
    // Update the first sheet with the latest data from Responses
    for (let j = 1; j < firstSheetData.length; j++) {
      const row = firstSheetData[j];
      const llave = row[llaveIndexFirstSheet];
      
      if (latestResponses[llave]) {
        const updatedData = latestResponses[llave];
        // Fix: Ensuring the column indices are correct for setting values
        firstSheet.getRange(j + 1, instrumentoIndexFirstSheet + 1).setValue(updatedData.instrumento);
        firstSheet.getRange(j + 1, soloGrupoIndexFirstSheet + 1).setValue(updatedData.soloGrupo);
        firstSheet.getRange(j + 1, vecesEvaluacionIndexFirstSheet + 1).setValue(updatedData.vecesEvaluacion);
        firstSheet.getRange(j + 1, mesesEvaluacionIndexFirstSheet + 1).setValue(updatedData.mesesEvaluacion);
      }
    }
    
    SpreadsheetApp.getUi().alert('Data updated successfully!');
  }
  