Sub FilterByType()
    Dim ws As Worksheet
    Dim rawDataWs As Worksheet
    Dim uniqueIdCol As Range, areaTypeCol As Range
    Dim uniqueIds As Object
    Dim selectedType As String
    Dim cell As Range
    Dim targetCol As Integer
    Dim idTypeMap As Object
    Dim typeList As String
    Dim typeArray() As String
    Dim lastRow As Long

    ' Set the RawData worksheet
    Set rawDataWs = ThisWorkbook.Sheets("RawData")

    ' Initialize a dictionary to map UniqueIDs to types
    Set idTypeMap = CreateObject("Scripting.Dictionary")

    ' Determine the last row with data in the UniqueID and Area Type columns
    lastRow = rawDataWs.Cells(rawDataWs.Rows.Count, 4).End(xlUp).Row

    ' Define the relevant columns with the actual range that contains data
    Set uniqueIdCol = rawDataWs.Range("C2:C" & lastRow) ' Column 4: UniqueID
    Set areaTypeCol = rawDataWs.Range("AG2:AG" & lastRow) ' Column 2: Clasificación por área

    ' Debug print to check if the columns are being set correctly
    Debug.Print "RawData worksheet set successfully."
    Debug.Print "UniqueID column: " & uniqueIdCol.Address
    Debug.Print "Area type column: " & areaTypeCol.Address

    ' Fill the dictionary with UniqueID-to-Type mapping
    For Each cell In uniqueIdCol
        If Not IsEmpty(cell.Value) Then
            Debug.Print "Processing UniqueID: " & cell.Value & ", Type: " & rawDataWs.Cells(cell.Row, 33).Value
            idTypeMap(cell.Value) = rawDataWs.Cells(cell.Row, 33).Value
        End If
    Next cell

    ' Debug print to check the dictionary contents
    Debug.Print "Dictionary populated with UniqueID-to-Type mapping:"
    For Each Key In idTypeMap.Keys
        Debug.Print "UniqueID: " & Key & ", Type: " & idTypeMap(Key)
    Next

    ' Collect unique types
    Set uniqueIds = CreateObject("Scripting.Dictionary")
    For Each Key In idTypeMap.Items
        If Not uniqueIds.exists(Key) Then
            uniqueIds.Add Key, Key
        End If
    Next

    ' Debug print to check unique types collection
    Debug.Print "Unique types collected:"
    For Each Key In uniqueIds.Keys
        Debug.Print Key
    Next

    ' Create a list of unique types as a string
    typeList = "Select a type from the following list:" & vbCrLf
    For Each Key In uniqueIds.Keys
        typeList = typeList & Key & vbCrLf
    Next

    ' Debug print to check the type list string
    Debug.Print "Type list created:" & vbCrLf & typeList

    ' Prompt the user to select a type from the list
    selectedType = InputBox(typeList, "Select a type")
    If selectedType = "" Then
        Debug.Print "No type selected. Exiting macro."
        Exit Sub
    End If

    ' Debug print to confirm the selected type
    Debug.Print "Selected type: " & selectedType

    For Each ws In ThisWorkbook.Worksheets
        If ws.Name <> "RawData" And ws.Name <> "P1 ASIGNATURA ABIERTA" And ws.Name <> "P5 ASIGNATURA ABIERTA" And ws.Name <> "P1. PROFESOR ABIERTA" And ws.Name <> "P2. PROFESOR ABIERTA" And ws.Name <> "P3. PROFESOR ABIERTA" And ws.Name <> " Aspectos Positivos Profesor " And ws.Name <> "Mejoras Profesor" And ws.Name <> "QuestionMapper" And ws.Name <> "P5 ASIGNATURA ABIERTA" Then
            ' Search for the "UniqueID" column within the first 4 columns
            Debug.Print ws.Name
            
            ' Loop through the columns 1 to 7 to find the "UniqueID" column
            For targetCol = 1 To 7
                ' Loop through the first 7 rows to check if the current column contains the "UniqueID" header
                For headerRow = 1 To 7
                    ' Debug.Print ws.Cells(headerRow, targetCol).Value
                    ' Debug.Print targetCol
                    If ws.Cells(headerRow, targetCol).Value = "UniqueID" Then
                        Debug.Print ws.Cells(headerRow, targetCol).Value
                        For i = ws.Cells(ws.Rows.Count, targetCol).End(xlUp).Row To headerRow + 1 Step -1
                            If ws.Cells(i, targetCol).Value <> "" Then
                                If idTypeMap.exists(ws.Cells(i, targetCol).Value) Then
                                    If idTypeMap(ws.Cells(i, targetCol).Value) <> selectedType Then
                                        ws.Rows(i).Delete
                                        ' Debug print to show which rows are being deleted
                                        Debug.Print "Row " & i & " deleted in sheet: " & ws.Name
                                    End If
                                End If
                            End If
                        Next i
                    End If
                Next headerRow
            Next targetCol

        End If
    Next ws
    MsgBox "Filtering complete!"
End Sub
