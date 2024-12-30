Sub Delete()
    Dim wsFirst As Worksheet
    Dim wsX As Worksheet
    Dim firstHeaders As Collection
    Dim lastColFirst As Long, lastColX As Long
    Dim colFirst As Long, colX As Long
    Dim header As Variant
    Dim matchingCol As Long

    ' Set the first sheet and sheet X
    Set wsFirst = ThisWorkbook.Sheets(1)
    Set wsX = ThisWorkbook.Sheets("SheetX") ' Replace "SheetX" with the name of your target sheet

    ' Get headers from the first sheet
    Set firstHeaders = New Collection
    lastColFirst = wsFirst.Cells(1, wsFirst.Columns.Count).End(xlToLeft).Column

    On Error Resume Next ' Avoid error if adding duplicate keys
    For colFirst = 1 To lastColFirst
        header = wsFirst.Cells(1, colFirst).Value
        If header <> "" Then
            firstHeaders.Add header, CStr(header)
        End If
    Next colFirst
    On Error GoTo 0

    ' Get headers from sheet X
    lastColX = wsX.Cells(1, wsX.Columns.Count).End(xlToLeft).Column

    ' Loop through each column in sheet X to find matches with the first sheet
    For colX = 1 To lastColX
        header = wsX.Cells(1, colX).Value

        ' Check if the header exists in the first sheet's headers
        If IsInCollection(firstHeaders, header) Then
            ' Get the matching column in the first sheet
            matchingCol = wsFirst.Cells(1, wsFirst.Columns.Count).End(xlToLeft).Column
            For colFirst = 2 To matchingCol
                If wsFirst.Cells(1, colFirst).Value = header Then
                    matchingCol = colFirst
                    Exit For
                End If
            Next colFirst

            wsFirst.Range(wsFirst.Cells(2, matchingCol), wsFirst.Cells(300, matchingCol)).ClearContents
        End If
    Next colX

    MsgBox "Data cleared for matching columns in the first sheet.", vbInformation
End Sub

' Function to check if a header exists in the collection
Function IsInCollection(coll As Collection, key As Variant) As Boolean
    On Error Resume Next
    IsInCollection = Not IsEmpty(coll.Item(CStr(key)))
    On Error GoTo 0
End Function
