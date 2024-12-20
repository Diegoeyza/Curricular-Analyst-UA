Sub CheckCourseIntersections()
    Dim wb1 As Workbook, wb2 As Workbook
    Dim ws1 As Worksheet, ws2 As Worksheet
    Dim rng1 As Range, rng2 As Range, filterRange As Range
    Dim cell1 As Range, cell2 As Range
    Dim nrc1 As String, nrc2 As String
    Dim filteredNRC As Object
    Dim tipo1 As String, tipo2 As String
    Dim dayHeaders As Variant
    Dim start1 As Date, end1 As Date, start2 As Date, end2 As Date
    Dim dia1 As String, dia2 As String
    Dim intersectionList As Collection
    Dim filePath As String
    Dim outputCol As Integer
    Dim result As String
    Dim i As Integer
    
    ' Initialize constants
    dayHeaders = Array("LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES")

    
    ' Set workbook and worksheet for the first Excel
    Set wb1 = ThisWorkbook
    Set ws1 = wb1.Sheets("Sheet1")
    Set rng1 = ws1.Range("A1:A" & ws1.Cells(ws1.Rows.Count, "A").End(xlUp).Row) ' Range including NRC1 and NRC2
    
    ' Open the second Excel
    filePath = Application.GetOpenFilename("Excel Files (*.xls; *.xlsx), *.xls; *.xlsx", , "Select the Second Workbook")
    If filePath = "False" Then Exit Sub ' Exit if no file is selected
    Set wb2 = Workbooks.Open(filePath)
    Set ws2 = wb2.Sheets(1) ' Adjust sheet index or name as needed
    Set filterRange = ws2.Rows(14) ' Assume headers are in row 14

    ' Loop through NRC pairs in the first workbook
    For Each cell1 In rng1
        nrc1 = ws1.Cells(cell1.Row, ws1.Columns("NRC1").Column).Value
        nrc2 = ws1.Cells(cell1.Row, ws1.Columns("NRC2").Column).Value
        outputCol = ws1.Columns("tope").Column
        
        ' Filter the second workbook's NRC column
        With ws2
            .AutoFilterMode = False
            filterRange.AutoFilter Field:=filterRange.Columns("NRC").Column, Criteria1:=Array(nrc1, nrc2), Operator:=xlFilterValues
        End With
        
        ' Collect filtered rows into a collection
        Set filteredNRC = CreateObject("Scripting.Dictionary")
        For Each cell2 In ws2.Range("NRC:NRC").SpecialCells(xlCellTypeVisible).Offset(1, 0) ' Skip header row
            filteredNRC(cell2.Value) = cell2.Row
        Next cell2
        
        ' Check time and date intersections
        Set intersectionList = New Collection
        For Each nrcKey In filteredNRC.Keys
            For i = LBound(dayHeaders) To UBound(dayHeaders)
                ' Get timetable data for both courses
                start1 = TimeValue(ws1.Cells(filteredNRC(nrc1), ws1.Columns(dayHeaders(i)).Column).Value)
                end1 = TimeValue(ws1.Cells(filteredNRC(nrc1), ws1.Columns(dayHeaders(i) + 1).Column).Value)
                start2 = TimeValue(ws2.Cells(filteredNRC(nrcKey), ws2.Columns(dayHeaders(i)).Column).Value)
                end2 = TimeValue(ws2.Cells(filteredNRC(nrcKey), ws2.Columns(dayHeaders(i) + 1).Column).Value)
                
                ' Check for time overlap
                If (start1 < end2) And (end1 > start2) Then
                    tipo1 = ws1.Cells(filteredNRC(nrc1), ws1.Columns("TIPO DE REUNIÓN").Column).Value
                    tipo2 = ws2.Cells(filteredNRC(nrcKey), ws2.Columns("TIPO DE REUNIÓN").Column).Value
                    
                    ' Check "CLAS", "AYUD", "LABT"
                    If Not (tipo1 = "CLAS" Or tipo1 = "AYUD" Or tipo1 = "LABT") Or Not (tipo2 = "CLAS" Or tipo2 = "AYUD" Or tipo2 = "LABT") Then
                        dia1 = ws1.Cells(filteredNRC(nrc1), ws1.Columns("día").Column).Value
                        dia2 = ws2.Cells(filteredNRC(nrcKey), ws2.Columns("día").Column).Value
                        If dia1 = dia2 Then
                            intersectionList.Add tipo1 & "-" & tipo2
                        End If
                    Else
                        intersectionList.Add tipo1 & "-" & tipo2
                    End If
                End If
            Next i
        Next nrcKey
        
        ' Convert intersection list to string
        If intersectionList.Count > 0 Then
            result = ""
            For Each Item In intersectionList
                result = result & Item & ", "
            Next Item
            result = Left(result, Len(result) - 2) ' Remove trailing comma and space
        Else
            result = "No intersection"
        End If
        
        ' Write result to "tope" column in the first workbook
        ws1.Cells(cell1.Row, outputCol).Value = result
    Next cell1

    ' Cleanup
    ws2.AutoFilterMode = False
    wb2.Close SaveChanges:=False
    MsgBox "Processing completed!", vbInformation
End Sub

