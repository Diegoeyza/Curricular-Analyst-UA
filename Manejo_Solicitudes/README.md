
# CheckCourseIntersections Macro

## Overview
This VBA macro compares course schedules between two Excel workbooks to identify time and date intersections between pairs of courses. It outputs intersection details and the count of intersections for each pair into specified columns of the first workbook.

## File and Sheet Setup
### Workbook 1 (Requests Workbook)
- **Sheet Index**: The macro will use the first sheet (`Sheets(1)`).
- **Column Requirements**:
  - **NRC (colNRC1)**: Unique course identifier for the first course. Must have a header titled "NRC".
  - **NRC2 (colNRC2)**: Unique course identifier for the second course. Must have a header titled "TOPE DE HORARIO CURSO 2".
  - **Intersections Output Column (colTope)**: Outputs the intersection details (e.g., `CLAS-CLAS`). Must have a header titled "TOPES".
  - **Intersection Count Column (colCantidadTopes)**: Outputs the count of intersections. Must have a header titled "CANTIDAD TOPES".
  
### Workbook 2 (Schedule Workbook)
- **Sheet Index**: The macro will use the first sheet (`Sheets(1)`).
- **Row Requirements**:
  - **Header Row**: Assumed to be in row 14.
  - **Course Start Row**: Data starts from row 15.
- **Column Requirements**:
  - **NRC (colNRC)**: Unique course identifier for filtering rows.
  - **Course Type (colTipo)**: Type of course (e.g., `CLAS`, `AYUD`, `LABT`).
  - **Day Headers (dayHeaders)**: Days of the week (`LUNES`, `MARTES`, etc.).
  - **Start Date (colDia)**: Start date or day details for evaluations or courses.

## How to Run
1. Open **Workbook 1** (Requests Workbook) in Excel.
2. Ensure the first sheet is active and that the required columns are present.
3. Open the VBA editor (`Alt + F11`) and paste the macro into a module.
4. Run the macro:
   - Go to the Excel ribbon > `Developer` > `Macros`.
   - Select `CheckCourseIntersections` and click `Run`.
5. A file dialog will prompt you to select **Workbook 2** (Schedule Workbook). Choose the appropriate file and ensure the required sheet is the first one.

## Important Notes
1. **Column Headers**:
   - If the column names change, update the header names in the code:
     - `FindColumn(ws1, "NRC")`
     - `FindColumn(ws1, "TOPE DE HORARIO CURSO 2")`
     - `FindColumn(ws1, "TOPES")`
     - `FindColumn(ws1, "CANTIDAD TOPES")`
     - `FindColumn(ws2, "NRC", 14)`
     - `FindColumn(ws2, "TIPO DE REUNIÓN", 14)`
     - `FindColumn(ws2, "INICIO", 14)`
   - Update the day headers in `dayHeaders` (e.g., `Array("LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES")`).
2. **Date and Time Parsing**:
   - The macro assumes time ranges are formatted as `HH:MM-HH:MM`. Modify `ParseTimeRange` if the format differs.
3. **Output Columns**:
   - Ensure the "TOPES" and "CANTIDAD TOPES" columns exist in Workbook 1 before running the macro.
4. **Number of Rows**:
   - The number of rows to be analized is determined by the last cell in column 1, so if the last cell of column 1 is in row 200, the code will analize 200 rows

## Output
- **Intersection Details**:
  - The column titled "TOPES" in Workbook 1 will show details of intersecting course types (e.g., `CLAS-CLAS`).
- **Intersection Count**:
  - The column titled "CANTIDAD TOPES" in Workbook 1 will show the count of intersections for each pair.

## Error Handling
- If a required header is not found, the macro will display an error message.
- If the time range format is invalid, the macro will raise an error with the problematic range.

## Step by Step Video
[Step by Step Video in Spanish](https://youtu.be/FVZL9_V2nLw)
