Sub casiConcentraciones()
    Dim wsDatos As Worksheet
    Dim wsAsignaciones As Worksheet
    Dim ultimoRenglon As Long
    Dim i As Long, j As Long
    Dim cupos As Object
    Dim concentraciones As Variant
    Dim alumnoID As String
    Dim prioridad As Integer
    Dim prioridadAcademica As Integer
    Dim asignado As Boolean
    Dim restricciones As Object
    Dim concentracion As String
    Dim especialidad As String
    Dim asignados As Object
    Dim unassignedRow As Long
    
    ' Check if the "Asignaciones" sheet exists and delete it
    On Error Resume Next
    Application.DisplayAlerts = False
    Set wsAsignaciones = ThisWorkbook.Sheets("Asignaciones")
    If Not wsAsignaciones Is Nothing Then
        wsAsignaciones.Delete
    End If
    Application.DisplayAlerts = True
    On Error GoTo 0

    ' Create a new "Asignaciones" sheet
    Set wsDatos = ThisWorkbook.Sheets("Datos") ' Change "Datos" to the name of your sheet with information
    Set wsAsignaciones = ThisWorkbook.Sheets.Add
    wsAsignaciones.Name = "Asignaciones"
    Debug.Print ("-----------------------------")
    
    ' Ask for available slots for each concentration
    concentraciones = Array("Diseño y Análisis de Algoritmos", "Movilidad Urbana", "Modelación Matemática Aplicada", _
                            "Análisis de Circuitos", "Diseño Hidráulico", "Desarrollo de Aplicaciones Web", "Ingeniería de Bioprocesos")
    
    Set cupos = CreateObject("Scripting.Dictionary")
    For i = LBound(concentraciones) To UBound(concentraciones)
        Dim numCupos As Integer
        ' Get the number of slots from column 8 of "Restricciones" sheet instead of InputBox
        Set wsRestricciones = ThisWorkbook.Sheets("Restricciones")
        numCupos = wsRestricciones.Cells(i + 2, 8).Value ' Assuming the slots are in column 8
        Debug.Print (wsRestricciones.Cells(i + 2, 8).Value)
        cupos.Add LCase(Trim(concentraciones(i))), numCupos ' Convert to lowercase and trim spaces
        Debug.Print (LCase(Trim(concentraciones(i))))
    Next i
    Debug.Print ("End slots")
    
    ' Set restrictions by concentration and specialty
    Set restricciones = CreateObject("Scripting.Dictionary")
    restricciones.Add "Diseño y Análisis de Algoritmos", Array("Ciencia de la Computación")
    restricciones.Add "Movilidad Urbana", Array() ' No restrictions
    restricciones.Add "Modelación Matemática Aplicada", Array("Industrial")
    restricciones.Add "Análisis de Circuitos", Array("Eléctrica")
    restricciones.Add "Diseño Hidráulico", Array("Obras Civiles", "Ambiental")
    restricciones.Add "Desarrollo de Aplicaciones Web", Array("Ciencia de la Computación")
    restricciones.Add "Ingeniería de Bioprocesos", Array("Ambiental")
    
    ' Initialize the dictionary to track already assigned students
    Set asignados = CreateObject("Scripting.Dictionary")
    
    ' Copy headers to the assignment sheet
    wsAsignaciones.Range("A1:I1").Value = Array("Alumno", "Email", "RUT", "Especialidad", "Creación", "Concentración", "Estado", "Prioridad", "Prioridad Académica")
    
    ' Get the last row with data
    ultimoRenglon = wsDatos.Cells(wsDatos.Rows.Count, 1).End(xlUp).Row
    
    ' Variable to track where to add unassigned rows
    unassignedRow = ultimoRenglon + 1
    
    ' Assign concentrations
    For i = 2 To ultimoRenglon
        alumnoID = wsDatos.Cells(i, 3).Value ' Assume column C is the student's RUT
        especialidad = wsDatos.Cells(i, 4).Value ' Specialty column
        
        ' Check priority
        If IsNumeric(wsDatos.Cells(i, 7).Value) Then
            prioridad = wsDatos.Cells(i, 7).Value
        Else
            prioridad = 0 ' Assign a default value if not numeric
        End If
        
        prioridadAcademica = wsDatos.Cells(i, 10).Value ' Academic Priority column
        asignado = False
        
        ' Check if the student already has an assignment
        If Not asignados.exists(alumnoID) Then
            ' Check restrictions and assign the best available option
            For j = 1 To 3 ' Priorities 1, 2, and 3
                concentracion = LCase(Trim(wsDatos.Cells(i, 6).Value)) ' Read concentration from column F (column 6)
                
                ' Check if the student's specialty is restricted for the desired concentration
                If restricciones.exists(concentracion) Then
                    If IsInArray(especialidad, restricciones(concentracion)) Then
                        GoTo NextPriority ' Skip to the next priority if the concentration is restricted
                    End If
                End If
                
                ' Check if the concentration has assigned slots and if there are available slots
                If cupos.exists(concentracion) Then
                    If cupos(concentracion) > 0 Then
                        wsAsignaciones.Cells(i, 1).Resize(1, 9).Value = wsDatos.Cells(i, 1).Resize(1, 9).Value
                        wsAsignaciones.Cells(i, 6).Value = concentracion
                        wsAsignaciones.Cells(i, 7).Value = "Asignado"
                        wsAsignaciones.Cells(i, 8).Value = prioridad ' Add this line to store "Prioridad"
                        Debug.Print (wsAsignaciones.Cells(i, 1).Value)
                        
                        Debug.Print (concentracion)
                        cupos(concentracion) = cupos(concentracion) - 1
                        Debug.Print (cupos(concentracion))
                        asignado = True
                        asignados.Add alumnoID, True ' Mark the student as assigned
                        Exit For
                    End If
                Else
                    MsgBox "Error: The concentration " & concentracion & " does not have assigned slots.", vbExclamation
                End If
NextPriority:
            Next j
        End If
        
        ' If no assignment was possible, add the row and mark it in red
        If Not asignado Then
            wsAsignaciones.Cells(unassignedRow, 1).Resize(1, 9).Value = wsDatos.Cells(i, 1).Resize(1, 9).Value
            wsAsignaciones.Cells(unassignedRow, 7).Value = "No Asignado"
            wsAsignaciones.Cells(unassignedRow, 1).Resize(1, 9).Interior.Color = RGB(255, 0, 0) ' Mark the row in red
            unassignedRow = unassignedRow + 1
        End If
    Next i

    ' Call the function to remove duplicates
    RemoveDuplicates wsAsignaciones

    MsgBox "Assignment completed.", vbInformation
End Sub

' Auxiliary function to check if an element is in an array
Function IsInArray(valueToFind As Variant, arr As Variant) As Boolean
    Dim element As Variant
    On Error Resume Next
    For Each element In arr
        If element = valueToFind Then
            IsInArray = True
            Exit Function
        End If
    Next element
    IsInArray = False
End Function

Sub RemoveDuplicates(ws As Worksheet)
    Dim lastRow As Long
    Dim i As Long
    Dim alumnoDict As Object
    Dim rowsToDelete As Range
    Set alumnoDict = CreateObject("Scripting.Dictionary")

    lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row ' Last row with data

    ' Iterate from the first row to the last
    For i = 2 To lastRow ' Start from 2 to skip the header row
        Dim alumno As String
        alumno = ws.Cells(i, 1).Value ' Column A (Student)

        ' Check if the row is empty or if the student already exists
        If alumno = "" Or alumnoDict.exists(alumno) Then
            If rowsToDelete Is Nothing Then
                Set rowsToDelete = ws.Rows(i)
            Else
                Set rowsToDelete = Union(rowsToDelete, ws.Rows(i))
            End If
        Else
            alumnoDict.Add alumno, Nothing ' Add the student to the dictionary
        End If
    Next i

    ' Delete marked rows
    If Not rowsToDelete Is Nothing Then
        rowsToDelete.Delete
    End If
End Sub