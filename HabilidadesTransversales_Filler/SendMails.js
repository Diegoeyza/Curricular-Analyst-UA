function sendEmailsFromHT() {
    const sheetName = "HT"; // The name of the sheet
    const emailColumnName = "EMAIL PROFESOR 1"; // Name of the email column
    const infoCorreoColumnName = "INFO CORREO"; // Name of the column with comments
  
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
  
    if (emailColIndex === 0 || infoCorreoColIndex === 0) {
      Logger.log(`Columns "${emailColumnName}" or "${infoCorreoColumnName}" not found.`);
      return;
    }
  
    const dataRange = sheet.getRange(2, 1, sheet.getLastRow() - 1, sheet.getLastColumn());
    const data = dataRange.getValues();
  
    // Iterate over the rows
    data.forEach((row, rowIndex) => {
      const email = row[emailColIndex - 1]; // Email value
      const note = sheet.getRange(rowIndex + 2, infoCorreoColIndex).getNote(); // Comment (note)
  
      if (email && note) { // If email and note exist
        try {
          GmailApp.sendEmail(email, "Información", note);
          Logger.log(`Email sent to: ${email}`);
        } catch (error) {
          Logger.log(`Failed to send email to: ${email}. Error: ${error.message}`);
        }
      }
    });
  }
  