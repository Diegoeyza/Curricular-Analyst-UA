function doGet() {
    return HtmlService.createHtmlOutputFromFile('form');
  }
  
  function getRecommendations(input) {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('CourseData');
    const data = sheet.getDataRange().getValues();
    const headers = data[0];
    const llaveIndex = headers.indexOf('LLAVE'); // Get the column index for LLAVE
    
    if (llaveIndex === -1) throw new Error('Column "LLAVE" not found.');
  
    const courses = data.slice(1).map(row => row[llaveIndex]); // Extract "LLAVE" column
    return courses.filter(course => course.toLowerCase().includes(input.toLowerCase()));
  }
  
  function getCourseData(courseName) {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('CourseData');
    const data = sheet.getDataRange().getValues();
    const headers = data[0];
  
    // Get indices for the required columns
    const indices = {
      LLAVE: headers.indexOf('LLAVE'),
      SECCIONES: headers.indexOf('SECCIONES'),
      HabilidadesTransversales: headers.indexOf('Habilidades Transversales'),
      SignificadoHT: headers.indexOf('Significado HT a medir'),
      Implementacion: headers.indexOf('Implementación'),
      QuienEvalua: headers.indexOf('¿Quién evalúa?')
    };
  
    // Check if all indices are valid
    for (const [key, index] of Object.entries(indices)) {
      if (index === -1) throw new Error(`Column "${key}" not found.`);
    }
  
    // Filter rows that match the course name
    const rows = data.slice(1).filter(row => row[indices.LLAVE] === courseName);
  
    // Map the rows to objects based on the column indices
    return rows.map(row => ({
      LLAVE: row[indices.LLAVE],
      SECCIONES: row[indices.SECCIONES],
      HabilidadesTransversales: row[indices.HabilidadesTransversales],
      SignificadoHT: row[indices.SignificadoHT],
      Implementacion: row[indices.Implementacion],
      QuienEvalua: row[indices.QuienEvalua]
    }));
  }
  
  function saveResponses(response) {
    const sheetName = 'Responses';
    let sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
  
    // Create the sheet if it doesn't exist
    if (!sheet) {
      sheet = SpreadsheetApp.getActiveSpreadsheet().insertSheet(sheetName);
      sheet.appendRow(['LLAVE', 'SECCIONES', 'Habilidades Transversales', 'Significado HT a medir', 'Implementación', '¿Quién evalúa?', 'instrumento', '¿Cuántas veces durante el semestre se evalúa la HT?', 'comentarios']);
    }
  
    // Append the response to the sheet
    sheet.appendRow([
      response.LLAVE,
      response.SECCIONES,
      response.HabilidadesTransversales,
      response.SignificadoHT,
      response.Implementacion,
      response.QuienEvalua,
      response.instrumento,
      response.evaluations,
      response.comentarios
    ]);
  }
  