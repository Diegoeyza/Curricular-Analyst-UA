import pandas as pd
import textwrap
import networkx as nx
from pyvis.network import Network

# Load the Excel file
file_path = r"Curricular-Analyst-UA\Visualización_RA\data\RA Uandes.xlsx"
general_df = pd.read_excel(file_path, sheet_name="general")
requirements_df = pd.read_excel(file_path, sheet_name="requirements")
objectives_df = pd.read_excel(file_path, sheet_name="objectives")
ra_links_df = pd.read_excel(file_path, sheet_name="RA_Links")

# Create a directed graph
graph = nx.DiGraph()

# Add courses as nodes
for _, row in general_df.iterrows():
    course_id = row['ID']
    course_name = row['Nombre']
    graph.add_node(course_id, label=course_name, type="course")

# Add prerequisites as edges
for _, row in requirements_df.iterrows():
    course_id = row['ID']
    prereq_id = row['ID_Requisito']
    graph.add_edge(prereq_id, course_id, type="prerequisite")

# Add course objectives as nodes
for _, row in objectives_df.iterrows():
    course_id = row['ID']
    objective_id = row['ID_Objetivo']
    objective_name = row['Objetivo']

    # Ensure objective_name is a string and handle missing values
    if pd.isna(objective_name):
        objective_name = "No description available"
    else:
        objective_name = str(objective_name)

    # Use textwrap to wrap text at spaces
    max_line_length = 30  # Adjust line length as needed
    objective_name_wrapped = "\n".join(textwrap.wrap(objective_name, width=max_line_length))

    node_label = f"{course_id}-{objective_id}"
    graph.add_node(node_label, label=objective_name_wrapped, type="objective")
    graph.add_edge(course_id, node_label, type="has_objective")


# Add objective links as edges
for _, row in ra_links_df.iterrows():
    course_id = row['ID']
    objective_id = row['ID_Objetivo']
    linked_course_id = row['ID_Prerequisito']
    linked_objective_id = row['ID_Objetivo_Prerrequisito']
    importancia = row['Importancia']
    source_node = f"{course_id}-{objective_id}"
    target_node = f"{linked_course_id}-{linked_objective_id}"
    graph.add_edge(source_node, target_node, type="objective_link", importancia=importancia)

# Create an interactive Pyvis network
net = Network(height="1000px", width="100%", directed=True)

# Add nodes and edges with attributes
for node, data in graph.nodes(data=True):
    node_type = data.get("type", "unknown")
    label = data.get("label", str(node))
    
    if node_type == "course":
        net.add_node(
            node,
            label=label,
            color="lightblue",
            title="Course",
            font={"size": 24}  # Approximately 100% bigger for courses
        )
    elif node_type == "objective":
        net.add_node(
            node,
            label=label,
            color="lightgreen",
            title="Objective",
            hidden=True,  # Initially hidden
            font={"size": 21, "multi": True}  # 50% bigger and multiline for objectives
        )
    else:
        net.add_node(
            node,
            label=label,
            color="grey",
            title="Unknown",
            hidden=True
        )

# Add edges with customized colors
for source, target, data in graph.edges(data=True):
    edge_type = data.get("type", "unknown")
    importancia = data.get("importancia", "")

    # Set color based on edge type
    if edge_type == "prerequisite":
        # Use black for course prerequisite edges
        net.add_edge(source, target, color="black", title=importancia, label=importancia)
    elif edge_type == "has_objective":
        # Use blue for objective edges
        net.add_edge(source, target, color="blue", title=importancia, label=importancia)
    elif edge_type == "objective_link":
        # Use red for objective link edges
        net.add_edge(source, target, color="red", title=importancia, label=importancia)

# Set basic physics options
net.set_options("""
var options = {
  "physics": {
    "barnesHut": {
      "gravitationalConstant": -20000,
      "centralGravity": 0.3,
      "springLength": 95,
      "springConstant": 0.04,
      "damping": 0.09
    },
    "minVelocity": 20
  },
  "interaction": {
    "hover": true,
    "navigationButtons": true
  }
}
""")

# Save the graph
output_file = "curricular_graph.html"
net.save_graph(output_file)

# Add custom JavaScript for interactivity
with open(output_file, "r", encoding="utf-8") as file:
    html_content = file.read()

custom_js = """
<script type="text/javascript">
let defaultCourses = network.body.data.nodes.get().filter(node => node.title === "Course");
let defaultEdges = network.body.data.edges.get().filter(edge => edge.title === "Prerequisite");

// Reset view to show only courses and their prerequisite edges
function resetView() {
    // Show all courses
    let allCourses = network.body.data.nodes.get().filter(node => node.title === "Course");
    network.body.data.nodes.update(allCourses.map(node => ({ id: node.id, hidden: false })));

    // Hide all objectives
    let allObjectives = network.body.data.nodes.get().filter(node => node.title === "Objective");
    network.body.data.nodes.update(allObjectives.map(node => ({ id: node.id, hidden: true })));

    // Show only prerequisite edges (course-to-course)
    let allEdges = network.body.data.edges.get().map(edge => {
        const isPrerequisite = edge.color === "black"; // Assuming black is used for prerequisite edges
        return { id: edge.id, hidden: !isPrerequisite };
    });
    network.body.data.edges.update(allEdges);
}


// Add a reset button
const resetButton = document.createElement("button");
resetButton.innerText = "Reset View";

// Basic button styles
resetButton.style.position = "absolute";
resetButton.style.top = "10px";
resetButton.style.left = "10px";
resetButton.style.zIndex = "1000";
resetButton.style.padding = "10px 20px";
resetButton.style.fontSize = "16px";
resetButton.style.backgroundColor = "#007BFF";
resetButton.style.color = "white";
resetButton.style.border = "none";
resetButton.style.borderRadius = "5px";
resetButton.style.cursor = "pointer";
resetButton.style.transition = "background-color 0.3s, transform 0.2s";

// Hover effect
resetButton.onmouseover = () => {
    resetButton.style.backgroundColor = "#0056b3"; // Darker blue on hover
    resetButton.style.transform = "scale(1.05)"; // Slightly enlarge the button
};

resetButton.onmouseout = () => {
    resetButton.style.backgroundColor = "#007BFF"; // Original blue color
    resetButton.style.transform = "scale(1)"; // Reset size
};

resetButton.onclick = resetView;

document.body.appendChild(resetButton);

// Add a timer to freeze the gravitational effect after 10 seconds
setTimeout(() => {
    network.setOptions({
        physics: {
            enabled: false // Disable physics to prevent nodes from moving
        }
    });
}, 90000);

// Add a search input field
const searchInput = document.createElement("input");
searchInput.type = "text";
searchInput.placeholder = "Search for a course...";
searchInput.style.position = "absolute";
searchInput.style.top = "10px";
searchInput.style.left = "140px"; // Added spacing from the "Reset View" button
searchInput.style.zIndex = "1000";
searchInput.style.padding = "8px 12px";
searchInput.style.fontSize = "14px";
searchInput.style.border = "2px solid #007BFF"; // Added border with color
searchInput.style.borderRadius = "4px";
searchInput.style.boxShadow = "0 2px 4px rgba(0, 0, 0, 0.1)";
searchInput.style.outline = "none";
searchInput.style.transition = "box-shadow 0.3s, border-color 0.3s";

// Add a focus effect for the input
searchInput.addEventListener('focus', () => {
    searchInput.style.borderColor = "#0056b3"; // Darker border color on focus
    searchInput.style.boxShadow = "0 2px 8px rgba(0, 86, 179, 0.3)";
});

searchInput.addEventListener('blur', () => {
    searchInput.style.borderColor = "#007BFF"; // Reset to the original border color
    searchInput.style.boxShadow = "0 2px 4px rgba(0, 0, 0, 0.1)";
});

document.body.appendChild(searchInput);

// Add a container for search suggestions
const suggestionsContainer = document.createElement("div");
suggestionsContainer.style.position = "absolute";
suggestionsContainer.style.top = "40px";
suggestionsContainer.style.left = "140px"; // Align with the input field
suggestionsContainer.style.zIndex = "1000";
suggestionsContainer.style.border = "2px solid #007BFF"; // Added border with color
suggestionsContainer.style.backgroundColor = "#fff";
suggestionsContainer.style.maxHeight = "200px";
suggestionsContainer.style.overflowY = "auto";
suggestionsContainer.style.borderRadius = "4px";
suggestionsContainer.style.boxShadow = "0 2px 4px rgba(0, 0, 0, 0.1)";
suggestionsContainer.style.display = "none"; // Initially hidden
document.body.appendChild(suggestionsContainer);


// Function to show suggestions
function showSuggestions(matches) {
    suggestionsContainer.innerHTML = ""; // Clear previous suggestions
    if (matches.length > 0) {
        suggestionsContainer.style.display = "block";
        matches.forEach(course => {
            const suggestion = document.createElement("div");
            suggestion.textContent = course.label;
            suggestion.style.padding = "5px";
            suggestion.style.cursor = "pointer";
            suggestion.onclick = function() {
                network.focus(course.id, { scale: 1.5, animation: true });
                network.selectNodes([course.id]);
                suggestionsContainer.style.display = "none";
            };
            suggestionsContainer.appendChild(suggestion);
        });
    } else {
        suggestionsContainer.style.display = "none";
    }
}

// Event listener for the search input
searchInput.addEventListener("input", function() {
    const searchTerm = searchInput.value.trim().toLowerCase();
    if (searchTerm) {
        // Find matching courses based on the input
        let matches = defaultCourses.filter(course => course.label.toLowerCase().includes(searchTerm));
        showSuggestions(matches);
    } else {
        suggestionsContainer.style.display = "none"; // Hide suggestions if input is empty
    }
});

// Handle node clicks
network.on("click", function (params) {
    if (params.nodes.length > 0) {
        const clickedNode = network.body.data.nodes.get(params.nodes[0]);
        
        if (clickedNode.title === "Course") {
            // Show objectives and links related to this course
            let courseId = clickedNode.id;

            // Show objectives of the clicked course
            let courseObjectives = network.body.data.nodes.get().filter(node => 
                node.title === "Objective" && node.id.startsWith(courseId + "-")
            );

            // Hide all nodes initially
            network.body.data.nodes.update(network.body.data.nodes.get().map(node => ({ id: node.id, hidden: true })));

            // Show the clicked course
            network.body.data.nodes.update({ id: courseId, hidden: false });

            // Show objectives of the clicked course
            network.body.data.nodes.update(courseObjectives.map(obj => ({ id: obj.id, hidden: false })));

            // Show edges related to this course and its objectives
            let relevantEdges = network.body.data.edges.get().filter(edge =>
                edge.from === courseId || courseObjectives.some(obj => edge.from === obj.id || edge.to === obj.id)
            );
            network.body.data.edges.update(relevantEdges.map(edge => ({ id: edge.id, hidden: false })));
            } else if (clickedNode.title === "Objective") {
                // Handle objective click
                let objectiveId = clickedNode.id;
                let parentCourseId = objectiveId.split("-")[0]; // Extract the parent course ID

                // Find all objectives of the parent course
                let courseObjectives = network.body.data.nodes.get().filter(node =>
                    node.title === "Objective" && node.id.startsWith(parentCourseId + "-")
                );

                // Hide all nodes initially
                network.body.data.nodes.update(network.body.data.nodes.get().map(node => ({ id: node.id, hidden: true })));

                // Show the clicked objective
                network.body.data.nodes.update({ id: objectiveId, hidden: false });

                // Show the parent course
                network.body.data.nodes.update({ id: parentCourseId, hidden: false });

                // Show objectives and courses linked to the clicked objective
                let linkedEdges = network.body.data.edges.get().filter(edge =>
                    edge.from === objectiveId || edge.to === objectiveId
                );

                // Collect linked nodes (objectives and courses)
                let linkedNodes = new Set();
                linkedEdges.forEach(edge => {
                    linkedNodes.add(edge.from);
                    linkedNodes.add(edge.to);
                });

                // Ensure linked objectives and their parent courses are visible
                let nodesToShow = network.body.data.nodes.get().filter(node =>
                    linkedNodes.has(node.id) || (node.title === "Course" && linkedNodes.has(node.id))
                );

                // Update visibility for linked objectives and their parent courses
                nodesToShow.forEach(node => {
                    if (node.title === "Objective") {
                        let linkedParentCourseId = node.id.split("-")[0];
                        network.body.data.nodes.update({ id: linkedParentCourseId, hidden: false });
                    }
                    network.body.data.nodes.update({ id: node.id, hidden: false });
                });

                // Ensure edges pointing from linked objectives to their parent courses are visible
                let additionalEdges = [];
                nodesToShow.forEach(node => {
                    if (node.title === "Objective") {
                        let linkedParentCourseId = node.id.split("-")[0];
                        let edgeId = `${linkedParentCourseId}-${node.id}`;
                        additionalEdges.push({
                            from: linkedParentCourseId,
                            to: node.id
                        });
                    }
                });

                // Combine original linked edges with parent-course edges
                let allEdgesToShow = [...linkedEdges, ...additionalEdges];

                // Update edges to show only the relevant ones
                network.body.data.edges.update(network.body.data.edges.get().map(edge => ({
                    id: edge.id,
                    hidden: !allEdgesToShow.some(e => e.from === edge.from && e.to === edge.to),
                })));
            }

    }
});
</script>
"""

# Inject JavaScript into the HTML
html_content += custom_js

# Save the modified HTML file
with open(output_file, "w", encoding="utf-8") as file:
    file.write(html_content)

print(f"Graph saved as {output_file}")
