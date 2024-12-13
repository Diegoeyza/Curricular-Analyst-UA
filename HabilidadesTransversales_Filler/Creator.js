function extractAndInsertData() {
    const activeSheet = SpreadsheetApp.getActiveSpreadsheet();
    const targetSheetName = "HT";
    const targetSheet = activeSheet.getSheetByName(targetSheetName) || activeSheet.insertSheet(targetSheetName);
    targetSheet.clear(); // Limpia el contenido previo
  
    const sourceSpreadsheetId = "1o6HftjnQiU4EB1T9mwZ5FntfkZqy9Bj5wkZKbyHl-m0"; // Cambia esto al ID de tu spreadsheet origen
    const sourceSpreadsheet = SpreadsheetApp.openById(sourceSpreadsheetId);
    const sourceSheet = sourceSpreadsheet.getSheetByName("MAESTRO"); // Cambia si no es la primera hoja
  
    const sourceData = sourceSheet.getDataRange().getValues();
    const sourceHeaders = sourceData[0]; // Headers in the source sheet
    const sourceRows = sourceData.slice(1); // Data without headers
  
    // Required columns in target and corresponding headers from the source
    const requiredColumns = [
      "AREA", "PLAN DE ESTUDIO", "LLAVE", "NRC", "CONECTOR DE LIGA", "LC", "CODIGO",
      "MATERIA", "CURSO", "TITULO", "SECCIONES", "SCT-Chile", "Habilidades Transversales",
      "RUT PROFESOR 1", "NOMBRE PROFESOR BANNER 1 (PROFESOR PRINCIPAL SESIÓN 01)", "EMAIL PROFESOR 1",
      "TELEFONO PROFESOR 1", "RUT PROFESOR 2", "NOMBRE PROFESOR 2 (2DO PROFESOR - SESIÓN 02)",
      "EMAIL PROFESOR 2", "TELEFONO PROFESOR 2", "RUT PROFESOR LABT",
      "PROFESOR LABT (PROFESOR LABT SESIÓN 03)", "MAIL PROFESOR LABT",
      "Significado HT a medir", "Implementación", "¿Quién evalúa?", "Instrumento",
      "¿Evaluará de manera individual o grupal?", "¿Cuántas veces durante el semestre se evalúa la HT?",
      "¿En qué mes va a evaluar la HT?", "Estimación corrección del Centro Escritura", 
      "Respondió Profesor", "¿SE EVALUO?", "¿CÓMO?", "¿CUÁNTAS VECES?", "CUÁNDO ENVÓ", 
      "CUANDO SE CORRIGIÓ", "OBSERVACIONES", "COMENTARIOS REUNIÓN", "COMENTARIOS 2",
      "COMENTARIOS 3", "OBSERVACION NUEVA"
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
      const cursoMandante = cursoMandanteIndex !== undefined ? row[cursoMandanteIndex] : "";
      const habilidades = habilidadesIndex !== undefined ? row[habilidadesIndex] : "";
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
    targetSheet.getRange(1, 1, outputData.length+1, requiredColumns.length+1).setHorizontalAlignment("center");
  }
  