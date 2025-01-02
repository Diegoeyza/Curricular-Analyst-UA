function extractAndInsertData() {
  const activeSheet = SpreadsheetApp.getActiveSpreadsheet();
  const targetSheetName = "HT";
  const targetSheet = activeSheet.getSheetByName(targetSheetName) || activeSheet.insertSheet(targetSheetName);
  targetSheet.clear(); // Clean the old content

  const sourceSpreadsheetId = "1o6HftjnQiU4EB1T9mwZ5FntfkZqy9Bj5wkZKbyHl-m0"; // Cambia esto al ID de tu spreadsheet origen
  const sourceSpreadsheet = SpreadsheetApp.openById(sourceSpreadsheetId);
  const sourceSheet = sourceSpreadsheet.getSheetByName("MAESTRO"); // Cambia si no es la primera hoja

  const sourceData = sourceSheet.getDataRange().getValues();
  const sourceHeaders = sourceData[0]; // Headers in the source sheet
  const sourceRows = sourceData.slice(1); // Data without headers

  // Required columns in target and corresponding headers from the source (some of these arent in the master sheet)
  const requiredColumns = [
    "AREA", "PLAN DE ESTUDIO", "LLAVE", "NRC", "CONECTOR DE LIGA", "LC", "CODIGO",
    "MATERIA", "CURSO", "TITULO", "SECCIONES", "SCT-Chile", "Habilidades Transversales",
    "RUT PROFESOR 1", "NOMBRE PROFESOR BANNER 1 \n(PROFESOR PRINCIPAL SESIÓN 01)", "EMAIL PROFESOR 1",
    "TELEFONO PROFESOR 1", "RUT PROFESOR 2", "NOMBRE PROFESOR 2\n(2DO PROFESOR - SESIÓN 02)",
    "EMAIL PROFESOR 2", "TELEFONO PROFESOR 2", "RUT PROFESOR LABT",
    "PROFESOR LABT ", "MAIL PROFESOR LABT",
    "Significado HT a medir", "Implementación", "Evaluación de la HT", "¿Quién evalúa?", "Instrumento",
    "¿Evaluará de manera individual o grupal?", "¿Cuántas veces durante el semestre se evalúa la HT?",
    "¿En qué mes va a evaluar la HT?", "Estimación corrección del Centro Escritura", 
    "Respondió Profesor", "¿SE EVALUO?", "¿CÓMO?", "¿CUÁNTAS VECES?", "CUÁNDO ENVÓ", 
    "CUANDO SE CORRIGIÓ", "OBSERVACIONES", "COMENTARIOS REUNIÓN", "COMENTARIOS 2",
    "COMENTARIOS 3", "OBSERVACION NUEVA", "INFO CORREO"
  ];

  const requiredIndexes = requiredColumns.map(col => sourceHeaders.indexOf(col));

  const missingColumns = requiredColumns.filter((_, i) => requiredIndexes[i] === -1);
  if (missingColumns.length) {
    Logger.log("Faltan las siguientes columnas: " + missingColumns.join(", "));
  }

  // Create a map of source headers to their index
  const headerMap = {};
  sourceHeaders.forEach((header, index) => {
    headerMap[header] = index;
  });

  // Filter data based on conditions
  const filteredData = sourceRows.filter(row => {
    const cursoMandanteIndex = headerMap["CURSO MANDANTE"];
    const habilidadesIndex = headerMap["Habilidades Transversales"];
    const nrcIndex = headerMap["NRC"];
    
    const cursoMandante = cursoMandanteIndex !== undefined ? row[cursoMandanteIndex] : "";
    const habilidades = habilidadesIndex !== undefined ? row[habilidadesIndex] : "";
    let nrc = nrcIndex !== undefined ? row[nrcIndex] : "";

    // Check if NRC is a number, if not replace with "N/A"
    if (!/^\d+$/.test(nrc)) {  // Regex checks if NRC is all digits
      row[nrcIndex] = "N/A";  // Modify the NRC value in the row
    }

    // Return the row if "CURSO MANDANTE" is "si" and "Habilidades Transversales" is not empty
    return cursoMandante.toString().toLowerCase() === "si" && habilidades.toString().trim() !== "";
  });


  // Map filtered data to the required structure
  const outputData = filteredData.map(row => {
    const mappedRow = requiredColumns.map(colName => {
      if (colName === "LLAVE") {
        const titulo = row[headerMap["TITULO"]] || "";
        const nrc = row[headerMap["NRC"]] || "";
        return `${titulo} NRC ${nrc}`;
      }
      const index = headerMap[colName];
      return index !== undefined ? row[index] : "";
    });

    // Ensure all rows have the correct number of columns
    while (mappedRow.length < requiredColumns.length) {
      mappedRow.push("");
    }
    return mappedRow;
  });

  // Insert data into the target sheet
  targetSheet.getRange(1, 1, 1, requiredColumns.length).setValues([requiredColumns]);
  if (outputData.length) {
    targetSheet.getRange(2, 1, outputData.length, requiredColumns.length).setValues(outputData);
  }

  // Format the header row
  const headerRange = targetSheet.getRange(1, 1, 1, requiredColumns.length);
  headerRange.setFontWeight("bold"); // Make headers bold
  headerRange.setWrap(true); // Enable text wrapping for long headers
  targetSheet.setRowHeight(1, 40); // Set the header row height to 40 pixels
  targetSheet.setColumnWidths(1, requiredColumns.length, 100); // Auto-adjust column widths
  targetSheet.setColumnWidth(1, 125);
  targetSheet.setColumnWidth(3, 470);
  targetSheet.setColumnWidth(10, 317);
    targetSheet.setColumnWidth(16, 300);
  targetSheet.setColumnWidth(25,400);
  targetSheet.setColumnWidth(26, 195);
  targetSheet.setColumnWidth(27, 420);
  targetSheet.setColumnWidth(45, 150);
  targetSheet.getRange(1, 1, outputData.length + 1, requiredColumns.length + 1).setHorizontalAlignment("center");

  // Now, read the 'Habilidades Transversales' column and match in 'Diccionario'
  const habilidadesColumnIndex = requiredColumns.indexOf("Habilidades Transversales") + 1; // Column number (1-based index)
  const habilidadesValues = targetSheet.getRange(2, habilidadesColumnIndex, outputData.length, 1).getValues();

  const diccionarioSheet = activeSheet.getSheetByName("Diccionario"); // Get the Diccionario sheet
  const diccionarioData = diccionarioSheet.getDataRange().getValues(); // Get all data from Diccionario sheet
  const diccionarioHeaders = diccionarioData[0]; // Headers in the Diccionario sheet
  const siglaIndex = diccionarioHeaders.indexOf("Sigla"); // Index of the Sigla column
  const significadoIndex = diccionarioHeaders.indexOf("Significado");
  const implementacionIndex = diccionarioHeaders.indexOf("Implementación");
  const evaluacionIndex = diccionarioHeaders.indexOf("Evaluación de la HT");
  const correoIndex = diccionarioHeaders.indexOf("Correo");
  const quienEvaluaIndex = diccionarioHeaders.indexOf("¿Quién evalúa?");

  // Iterate over the 'Habilidades Transversales' and update matching rows
  for (let i = 0; i < habilidadesValues.length; i++) {
    const habilidadesStripped = habilidadesValues[i][0].replace(/\s+/g, ''); // Remove all spaces
    const habilidadesList = habilidadesStripped.split(","); // Split by commas

    let significadoFinal = "";
    let implementacionFinal = "";
    let evaluacionFinal = "";
    let correoFinal= "";
    let quienEvaluaFinal="";

    for (let habilidad of habilidadesList) {
      let diccionarioRow = diccionarioData.find(row => row[siglaIndex] === habilidad); // Find the matching row

      if (!diccionarioRow) {
        // If the habilidad is not found in Diccionario, add it
        diccionarioRow = [];
        diccionarioRow[siglaIndex] = habilidad; // Set the Sigla value

        // Add the new row to the Diccionario sheet
        diccionarioSheet.appendRow(diccionarioRow);
        diccionarioData.push(diccionarioRow); // Update in-memory data

        // Highlight the newly added row
        const lastRow = diccionarioSheet.getLastRow(); // Get the last row in the Diccionario sheet
        diccionarioSheet.getRange(lastRow, 1, 1, diccionarioHeaders.length) // Select the entire row
          .setBackground("#FFFF00"); // Highlight with yellow
      }


      // Extract data from the Diccionario sheet
      const significado = diccionarioRow[significadoIndex] || "";
      const implementacion = diccionarioRow[implementacionIndex] || "";
      const evaluacion = diccionarioRow[evaluacionIndex] || "";
      const correo = diccionarioRow[correoIndex] || "";
      const quienEvalua = diccionarioRow[quienEvaluaIndex] || "";

      // Concatenate the values with "y" for multiple matches
      if (significado) {
        if (significadoFinal) {
          significadoFinal += " y " + significado;
        } else {
          significadoFinal = significado;
        }
      }
      if (implementacion) {
        if (implementacionFinal) {
          implementacionFinal += " y " + implementacion;
        } else {
          implementacionFinal = implementacion;
        }
      }
      if (evaluacion) {
        if (evaluacionFinal) {
          evaluacionFinal += " y " + evaluacion;
        } else {
          evaluacionFinal = evaluacion;
        }
      }
      if (correo) {
        correoFinal = correo;
      }
      if (quienEvalua) {
        if (quienEvaluaFinal) {
          quienEvaluaFinal += " y " + quienEvalua;
        } else {
          quienEvaluaFinal = quienEvalua;
        }
      }
    }

    // Insert the concatenated results into the HT sheet
    const significadoCell = targetSheet.getRange(i + 2, requiredColumns.indexOf("Significado HT a medir") + 1);
    const implementacionCell = targetSheet.getRange(i + 2, requiredColumns.indexOf("Implementación") + 1);
    const evaluacionCell = targetSheet.getRange(i + 2, requiredColumns.indexOf("Evaluación de la HT") + 1);
    const correoCell = targetSheet.getRange(i + 2, requiredColumns.indexOf("INFO CORREO") + 1);
    const quienEvaluaCell = targetSheet.getRange(i+2, requiredColumns.indexOf("¿Quién evalúa?")+1);
    if (habilidadesList.length>1 && !diccionarioData.map(row => row[0]).includes(habilidadesStripped)){
      diccionarioRow = [];
      diccionarioRow[siglaIndex] = habilidadesStripped; // Set the Sigla value
      diccionarioRow[significadoIndex] = significadoFinal; // Set default or placeholder values
      diccionarioRow[implementacionIndex] = implementacionFinal;
      diccionarioRow[evaluacionIndex] = evaluacionFinal;
      diccionarioRow[quienEvaluaIndex] = quienEvaluaFinal;

      // Add the new row to the Diccionario sheet
      diccionarioSheet.appendRow(diccionarioRow);
      diccionarioData.push(diccionarioRow); // Update in-memory data
    }

    significadoCell.setValue(significadoFinal);
    implementacionCell.setValue(implementacionFinal);
    evaluacionCell.setValue(evaluacionFinal);
    quienEvaluaCell.setValue(quienEvaluaFinal);

    // Handle the INFO CORREO column
    if (correoFinal.trim()) {
      correoCell.setValue("Si"); // Set the cell value to "Si"
      correoCell.setComment(correoFinal); // Add the content as a comment
    } else {
      correoCell.setValue("No"); // Set the cell value to "No"
      correoCell.clearNote(); // Remove any existing comment if content is empty
    }
  }
}