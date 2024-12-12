# Horarios_curso

## Steps:
1. **Prepare the Input File**:
   - Ensure your timetable file has:
     - Days of the week (Monday to Friday) and hours in the first two rows.
     - Course entries in the format: `ELECTRO (LAB) SEC 1;MARTES;9:30;10:20`.
     - **Important**: The course name should:
       - Not contain commas.
       - Have a space between the name and type (e.g., `ELECTRO (CLAS)`).
     - Invalid examples:
       - `ELECTRO(CLAS)` → Missing space.
       - `ELECTRO ( CLAS)` → Extra spaces.

2. **Set File Paths**:
   - Add your timetable file path to **line 5** of [`main.py`](https://github.com/Diegoeyza/Curricular-Analyst-UA/blob/a79c77a4c8fcb8e9cb2623926d34b067f64dffac/Horarios_curso/main.py#L5).
   - Convert your "Programación maestro macro" Excel file to CSV (only the DPSI sheet) and add its path to **line 9** of [`main.py`](https://github.com/Diegoeyza/Curricular-Analyst-UA/blob/a79c77a4c8fcb8e9cb2623926d34b067f64dffac/Horarios_curso/main.py#L9).

3. **Run the Code**:
   - Execute [`main.py`](Horarios_curso/main.py). It will generate:
     - **`Programación Maestro final.csv`**: Updated timetable with assigned schedules (rows without schedules are marked in red).
     - **`Missing_pairs.txt`**: Contains unmatched timetables with their details.

### Not Admitted Formats:
| Incorrect Format                | Correct Format               |
|---------------------------------|------------------------------|
| `SIMULACION (LAB) SEC 1 (LAB )` | `SIMULACION (LAB) SEC 1`     |
| `SIMULACION (LAB) SEC1`         | `SIMULACION (LAB) SEC 1`     |

4. **Modify Equivalences**:
   - Update the dictionary of equivalences in [`iterator.py`](Horarios_curso/iterator.py) as needed:
     - Add new entries.
     - Delete conflicting entries (recommended to recreate the dictionary if necessary).