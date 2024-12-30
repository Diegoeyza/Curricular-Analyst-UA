Sub CheckHeaders()
    Dim wsFirst As Worksheet
    Dim ws As Worksheet
    Dim firstHeaders As Collection
    Dim lastCol As Long
    Dim col As Long
    Dim header As Variant
    Dim found As Boolean
    Dim msg As String

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

    ' Loop through each header in the first sheet
    For Each header In firstHeaders
        found = False

        ' Check all other sheets for the header
        For Each ws In ThisWorkbook.Sheets
            If ws.Name <> wsFirst.Name Then
                lastCol = ws.Cells(1, ws.Columns.Count).End(xlToLeft).Column
                For col = 1 To lastCol
                    If ws.Cells(1, col).Value = header Then
                        found = True
                        Exit For
                    End If
                Next col
                If found Then Exit For
            End If
        Next ws

        ' If the header is not found in any sheet
        If Not found Then
            msg = msg & "Header '" & header & "' is missing in all other sheets." & vbNewLine
        End If
    Next header

    ' Display results
    If msg = "" Then
        MsgBox "All headers from the first sheet are present in at least one other sheet.", vbInformation
    Else
        MsgBox "Missing headers:" & vbNewLine & msg, vbExclamation
        Debug.Print "Missing headers:" & vbNewLine & msg
    End If
End Sub