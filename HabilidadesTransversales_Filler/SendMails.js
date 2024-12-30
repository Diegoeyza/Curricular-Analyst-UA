function sendEmailsFromHT() {
  const sheetName = "HT"; // The name of the sheet
  const emailColumnName = "EMAIL PROFESOR 1"; // Name of the email column
  const infoCorreoColumnName = "INFO CORREO"; // Name of the column with comments
  const cursoColumnName = "LLAVE"; // Name of the column with the course keys

  // Columns to check for emptiness
  const columnsToCheck = [
    "Instrumento",
    "¿Evaluará de manera individual o grupal?",
    "¿Cuántas veces durante el semestre se evalúa la HT?",
    "¿En qué mes va a evaluar la HT?"
  ];

  // Get the sheet
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
  if (!sheet) {
    Logger.log(`Sheet "${sheetName}" not found.`);
    return;
  }

  // Get the data
  const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  const emailColIndex = headers.indexOf(emailColumnName) + 1;
  const infoCorreoColIndex = headers.indexOf(infoCorreoColumnName) + 1;
  const cursoColIndex = headers.indexOf(cursoColumnName) + 1;

  const columnIndexesToCheck = columnsToCheck.map(col => headers.indexOf(col) + 1);

  if (
    emailColIndex === 0 || infoCorreoColIndex === 0 || cursoColIndex === 0 ||
    columnIndexesToCheck.includes(0)
  ) {
    Logger.log(`One or more required columns not found.`);
    return;
  }

  const dataRange = sheet.getRange(2, 1, sheet.getLastRow() - 1, sheet.getLastColumn());
  const data = dataRange.getValues();

  // Iterate over the rows
  data.forEach((row, rowIndex) => {
    const email = row[emailColIndex - 1]; // Email value
    const note = sheet.getRange(rowIndex + 2, infoCorreoColIndex).getNote(); // Comment (note)
    const course = row[cursoColIndex - 1]; // Course name

    // Check if all specified columns are empty
    const areColumnsEmpty = columnIndexesToCheck.every(index => !row[index - 1]);

    if (email && note && areColumnsEmpty) { // If email, note, and all columns are empty
      try {
        GmailApp.sendEmail(email, 'Formulario Habilidades Transversales para ' + course, note);
        Logger.log(`Email sent to: ${email}`);
      } catch (error) {
        Logger.log(`Failed to send email to: ${email}. Error: ${error.message}`);
      }
    }
  });
}
