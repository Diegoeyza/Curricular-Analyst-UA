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
    Set wsDatos = ThisWorkbook.Sheets("Datos") ' Cambia "Datos" por el nombre de tu hoja con la información
    Set wsAsignaciones = ThisWorkbook.Sheets.Add
    wsAsignaciones.Name = "Asignaciones"
    Debug.Print ("-----------------------------")
    
    ' Pregunta por los cupos disponibles para cada concentración
    concentraciones = Array("Diseño y Análisis de Algoritmos", "Movilidad Urbana", "Modelación Matemática Aplicada", _
                            "Análisis de Circuitos", "Diseño Hidráulico", "Desarrollo de Aplicaciones Web", "Ingeniería de Bioprocesos")
    
    Set cupos = CreateObject("Scripting.Dictionary")
    For i = LBound(concentraciones) To UBound(concentraciones)
        Dim numCupos As Integer
        ' Get the number of slots from column 7 of "Restricciones" sheet instead of InputBox
        Set wsRestricciones = ThisWorkbook.Sheets("Restricciones")
        numCupos = wsRestricciones.Cells(i + 2, 8).Value ' Assuming the cupos are in column 7
        Debug.Print (wsRestricciones.Cells(i + 2, 8).Value)
        cupos.Add LCase(Trim(concentraciones(i))), numCupos ' Convierte a minúsculas y elimina espacios
        Debug.Print (LCase(Trim(concentraciones(i))))
    Next i
    Debug.Print ("End cupos")
    
    ' Configura las restricciones por concentración y especialidad
    Set restricciones = CreateObject("Scripting.Dictionary")
    restricciones.Add "Diseño y Análisis de Algoritmos", Array("Ciencia de la Computación")
    restricciones.Add "Movilidad Urbana", Array() ' Sin restricciones
    restricciones.Add "Modelación Matemática Aplicada", Array("Industrial")
    restricciones.Add "Análisis de Circuitos", Array("Eléctrica")
    restricciones.Add "Diseño Hidráulico", Array("Obras Civiles", "Ambiental")
    restricciones.Add "Desarrollo de Aplicaciones Web", Array("Ciencia de la Computación")
    restricciones.Add "Ingeniería de Bioprocesos", Array("Ambiental")
    
    ' Inicializa el diccionario para rastrear los RUT de alumnos ya asignados
    Set asignados = CreateObject("Scripting.Dictionary")
    
    ' Copiar encabezados a la hoja de asignaciones
    wsAsignaciones.Range("A1:J1").Value = Array("Alumno", "Email", "RUT", "Especialidad", "Concentración", "Prioridad", "Estado", "Prioridad Académica")
    
    ' Obtener el último renglón con datos
    ultimoRenglon = wsDatos.Cells(wsDatos.Rows.Count, 1).End(xlUp).Row
    
    ' Variable to track where to add unassigned rows
    unassignedRow = ultimoRenglon + 1
    
    ' Asignar concentraciones
    For i = 2 To ultimoRenglon
        alumnoID = wsDatos.Cells(i, 3).Value ' Asume que la columna C es el RUT del alumno
        especialidad = wsDatos.Cells(i, 4).Value ' Columna de Especialidad
        
        ' Verificación de la prioridad
        If IsNumeric(wsDatos.Cells(i, 7).Value) Then
            prioridad = wsDatos.Cells(i, 7).Value
        Else
            prioridad = 0 ' Asigna un valor predeterminado si no es numérico
        End If
        
        prioridadAcademica = wsDatos.Cells(i, 10).Value ' Columna de Prioridad Académica
        asignado = False
        
        ' Verificar si el alumno ya tiene una asignación
        If Not asignados.exists(alumnoID) Then
            ' Verificar restricciones y asignar la mejor opción disponible
            For j = 1 To 3 ' Prioridades 1, 2, y 3
                concentracion = LCase(Trim(wsDatos.Cells(i, 6).Value)) ' Lee la concentración desde la columna F (columna 6)
                
                ' Verificar si la especialidad del alumno tiene restricción para la concentración deseada
                If restricciones.exists(concentracion) Then
                    If IsInArray(especialidad, restricciones(concentracion)) Then
                        GoTo SiguientePrioridad ' Saltar a la siguiente prioridad si la concentración está restringida
                    End If
                End If
                
                ' Verificar si la concentración tiene cupos asignados y si hay cupos disponibles
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
                        asignados.Add alumnoID, True ' Marca al alumno como asignado
                        Exit For
                    End If
                Else
                    MsgBox "Error: La concentración " & concentracion & " no tiene cupos asignados.", vbExclamation
                End If
SiguientePrioridad:
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

    MsgBox "Asignación completada.", vbInformation
End Sub

' Función auxiliar para verificar si un elemento está en un arreglo
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

    lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row ' Última fila con datos

    ' Iterar desde la primera fila hacia la última
    For i = 2 To lastRow ' Start from 2 to skip the header row
        Dim alumno As String
        alumno = ws.Cells(i, 1).Value ' Columna A (Alumno)

        ' Verificar si la fila está vacía o si el alumno ya existe
        If alumno = "" Or alumnoDict.exists(alumno) Then
            If rowsToDelete Is Nothing Then
                Set rowsToDelete = ws.Rows(i)
            Else
                Set rowsToDelete = Union(rowsToDelete, ws.Rows(i))
            End If
        Else
            alumnoDict.Add alumno, Nothing ' Agregar el alumno al diccionario
        End If
    Next i

    ' Eliminar filas marcadas
    If Not rowsToDelete Is Nothing Then
        rowsToDelete.Delete
    End If
End Sub
