Sub CheckHeadersAndColumns()
    Dim wsFirst As Worksheet
    Dim ws As Worksheet
    Dim firstHeaders As Collection
    Dim lastCol As Long
    Dim col As Long
    Dim header As Variant
    Dim matchingHeaders As Collection
    Dim msg As String
    Dim foundHeaders As String

    ' Set the first worksheet
    Set wsFirst = ThisWorkbook.Sheets(1)

    ' Get headers from the first worksheet
    Set firstHeaders = New Collection
    lastCol = wsFirst.Cells(1, wsFirst.Columns.Count).End(xlToLeft).Column

    On Error Resume Next ' Avoid error if adding duplicate keys
    For col = 1 To lastCol
        header = wsFirst.Cells(1, col).Value
        If header <> "" Then
            firstHeaders.Add header, CStr(header)
        End If
    Next col
    On Error GoTo 0

    ' Loop through each worksheet
    For Each ws In ThisWorkbook.Sheets
        If ws.Name <> wsFirst.Name Then
            Set matchingHeaders = New Collection
            lastCol = ws.Cells(1, ws.Columns.Count).End(xlToLeft).Column
            foundHeaders = ""

            ' Check for matching headers in the current sheet
            For col = 1 To lastCol
                header = ws.Cells(1, col).Value
                If IsInCollection(firstHeaders, header) Then
                    matchingHeaders.Add header
                    foundHeaders = foundHeaders & header & " (Column " & col & ")" & vbNewLine
                End If
            Next col

            ' If matching headers are found, add them to the message
            If foundHeaders <> "" Then
                msg = msg & "In sheet '" & ws.Name & "', the following headers match with the first sheet:" & vbNewLine & foundHeaders & vbNewLine
            Else
                msg = msg & "In sheet '" & ws.Name & "', no headers match the first sheet." & vbNewLine
            End If
        End If
    Next ws

    ' Display results
    If msg = "" Then
        MsgBox "All sheets have at least one matching header with the first sheet.", vbInformation
    Else
        MsgBox "Matching headers and columns:" & vbNewLine & msg, vbInformation
        Debug.Print "Matching headers and columns:" & vbNewLine & msg
    End If
End Sub

' Function to check if a header exists in the collection
Function IsInCollection(coll As Collection, key As Variant) As Boolean
    On Error Resume Next
    IsInCollection = Not IsEmpty(coll.Item(CStr(key)))
    On Error GoTo 0
End Function

