
# README: Curriculum Structure Visualization

## Description
This project uses Python and libraries such as `pandas`, `networkx`, and `pyvis` to create an interactive graph representing the structure of courses and objectives in an academic program. The graph includes nodes representing courses and objectives, as well as edges showing their relationships, such as prerequisites and links between objectives.

## Requirements
- Python 3.x
- Python libraries:
  - `pandas`
  - `networkx`
  - `pyvis`
  - `textwrap` (standard library)

## Installing Dependencies
Make sure to install the required libraries by running the following command:

```bash
pip install pandas networkx pyvis
```

## Code Usage

### 1. Preparing the Data
The code assumes you have an Excel file (`RA Uandes.xlsx`) containing the following sheets:

- `general`: information about the courses.
- `requirements`: prerequisites for the courses.
- `objectives`: objectives of the courses.
- `RA_Links`: links between objectives and their importance.

Ensure that the Excel file is located in the specified path (`Curricular-Analyst-UA\Visualización_RA\data\RA Uandes.xlsx`), or adjust the path in the code as needed.

### 2. Running the Script
Run the Python script to generate the interactive graph:

```bash
python script_name.py
```

This will create an HTML file named `curricular_graph.html` containing the visualization.

### 3. Viewing the Graph
To view the visualization, simply open the HTML file in your web browser. You can do this in one of the following ways:

- **File Explorer**: Double-click on the `curricular_graph.html` file.
- **Terminal**:
  - On Unix/Linux/Mac systems:
    ```bash
    open curricular_graph.html
    ```
  - On Windows:
    ```bash
    start curricular_graph.html
    ```

## Interactivity of the Visualization
The visualization includes the following interactive features:

- **Navigation and Zoom**: You can move and zoom in the graph to explore the courses and their objectives.
- **"Reset View" Button**: Resets the view to show only the courses and their prerequisites.
- **Search Field**: Allows you to search for courses by name. Matching courses will be shown in a suggestion list and highlighted when clicked.
- **Clicking on Nodes**:
  - Clicking on a course node will display its objectives and relevant edges.
  - Clicking on an objective node will show related courses and other objectives.

## Customization
You can modify the script to adjust the appearance and behavior of the graph. Some possible customizations include:

- Changing the colors of nodes and edges.
- Adjusting font size and style.
- Modifying physics options to change node behavior (there is a version called Graph_Gravity that does not disable the gravitational effect).
