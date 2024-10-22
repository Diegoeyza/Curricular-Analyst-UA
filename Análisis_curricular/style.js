
function fit() {
    var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    var newSheet = spreadsheet.getSheetByName("Course Dropdown");

    newSheet.setColumnWidth(1,250);
    newSheet.setColumnWidth(2,350);
    newSheet.setColumnWidth(4,250);
    newSheet.setColumnWidth(5,350);

    newSheet.setRowHeights(1,2,100);

    newSheet.getRange(1, 1, 2, 5).setVerticalAlignment("middle");
    newSheet.getRange(2, 1, 2, 5).setWrap(true);
}