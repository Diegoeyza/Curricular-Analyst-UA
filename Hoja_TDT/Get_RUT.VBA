Sub CopyRUT()
    Dim sourceSheet As Worksheet
    Dim destinationSheet As Worksheet
    Dim lastRow As Long

    ' Set the source and destination sheets
    Set sourceSheet = ThisWorkbook.Sheets("PT2 202420") ' Change to your source sheet name
    Set destinationSheet = ThisWorkbook.Sheets("Maestro") ' Change to your destination sheet name

    ' Find the last row in the source sheet's first column
    lastRow = sourceSheet.Cells(sourceSheet.Rows.Count, 1).End(xlUp).Row

    ' Copy the first column to the destination sheet
    sourceSheet.Range("A1:A" & lastRow).Copy
    destinationSheet.Range("A1").PasteSpecial Paste:=xlPasteValues

    ' Clear the clipboard
    Application.CutCopyMode = False

    MsgBox "First column copied successfully!", vbInformation
End Sub