import pandas as pd
import textwrap
import networkx as nx
from pyvis.network import Network

# Load the Excel file
file_path = r"C:\Users\diego\OneDrive\Documentos\Pythonhw\.vs\Curricular_analyst_UA\postgres_export.xlsx"
# Load and normalize column headers to lowercase for all DataFrames
general_df = pd.read_excel(file_path, sheet_name="general")
general_df.columns = [col.lower() for col in general_df.columns]
requirements_df = pd.read_excel(file_path, sheet_name="requirements")
requirements_df.columns = [col.lower() for col in requirements_df.columns]
objectives_df = pd.read_excel(file_path, sheet_name="objectives")
objectives_df.columns = [col.lower() for col in objectives_df.columns]
ra_links_df = pd.read_excel(file_path, sheet_name="RA_Links")
ra_links_df.columns = [col.lower() for col in ra_links_df.columns]

# Create a directed graph
graph = nx.DiGraph()

# Add courses as nodes
for _, row in general_df.iterrows():
    course_id = row['id']
    course_name = row['nombre']
    graph.add_node(course_id, label=course_name, type="course")

# Add prerequisites as edges
for _, row in requirements_df.iterrows():
    course_id = row['id']
    prereq_id = row['id_requisito']
    graph.add_edge(prereq_id, course_id, type="prerequisite")

# Add course objectives as nodes
for _, row in objectives_df.iterrows():
    course_id = row['id']
    objective_id = row['id_objetivo']
    objective_name = row['objetivo']

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
    course_id = row['id']
    objective_id = row['id_objetivo']
    linked_course_id = row['id_prerrequisito']
    linked_objective_id = row['id_objetivo_prerrequisito']
    importancia = row['importancia']
    source_node = f"{course_id}-{objective_id}"
    target_node = f"{linked_course_id}-{linked_objective_id}"
    graph.add_edge(target_node, source_node, type="objective_link", importancia=importancia)

# Create an interactive Pyvis network
net = Network(height="1000px", width="100%", directed=True, bgcolor="#1e1e1e", font_color="white")


# Add nodes and edges with attributes
for node, data in graph.nodes(data=True):
    node_type = data.get("type", "unknown")
    label = data.get("label", str(node))

    if node_type == "course":
        net.add_node(
            node,
            label=label,
            color="#1340bf",
            title="Course",
            font={"size": 100},  # 100% bigger for courses
            shape="hexagon",  # For rounded courses
            borderWidth=3,  # Thicker border
            borderWidthSelected=5,  # Even thicker when selected
            borderColor="#004aad",  # A color that complements the main node color
            shadow=True,
            size=40,
        )
    elif node_type == "objective":
        net.add_node(
            node,
            label=label,
            color="#90EE90",  # Bright green color for objectives
            title="Objective",  # Tooltip text
            font={
                "size": 21,  # Font size for objectives
                "multi": True,  # Support multiline labels
                "face": "Arial",  # Ensures consistent font style
                "color": "white",  # Contrast with bright background
            },
            shape="ellipse",  # Default shape for objectives
            borderWidth=4,  # Slightly thinner border than courses
            borderWidthSelected=4,  # Thicker when selected
            borderColor="green",  # Darker green border for emphasis
            shadow=True,  # Enable shadow for a 3D effect
            hidden=True,
        )

    else:
        net.add_node(
            node,
            label=label,
            color="grey",  # Neutral color for unknown types
            title="Unknown",
            hidden=True
        )

# Add edges with customized colors
for source, target, data in graph.edges(data=True):
    edge_type = data.get("type", "unknown")
    importancia = data.get("importancia", "")
    
    if edge_type == "prerequisite":
        net.add_edge(
            source,
            target,
            color="white",  # High contrast for dark backgrounds
            title=importancia,
            label=importancia,
            width=5,  # Medium thickness
            hoverWidth=6,  # Thicker when hovered
            font={"size": 14, "color": "white"},  # Readable font
        )
    elif edge_type == "has_objective":
        net.add_edge(
            source,
            target,
            color="#FF7F11",  # Bright orange for objectives
            title=importancia,
            label=importancia,
            width=3,  # Slightly thicker
            hoverWidth=4,
            font={"size": 14, "color": "#FF7F11"},  # Matching label color
        )
    elif edge_type == "objective_link":
        net.add_edge(
            source,
            target,
            color="red",  # Bright red for critical links
            title=importancia,
            label=importancia,
            width=4,  # Thick edge for emphasis
            hoverWidth=5,
            font={"size": 14, "color": "black"},
        )

'''
for source, target, data in graph.edges(data=True):
    edge_type = data.get("type", "unknown")
    importancia = data.get("importancia", "")

    if edge_type == "prerequisite":
        net.add_edge(source, target, color="white", title=importancia, label=importancia)  # White for better contrast
    elif edge_type == "has_objective":
        net.add_edge(source, target, color="#FF7F11", title=importancia, label=importancia)  # Cyan for objective links
    elif edge_type == "objective_link":
        net.add_edge(source, target, color="red", title=importancia, label=importancia)  # Red for critical links
'''

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
output_file = "curricular_graph_dark.html"
net.save_graph(output_file)

# Add custom JavaScript for interactivity
with open(output_file, "r", encoding="utf-8") as file:
    html_content = file.read()

custom_js = """
<script type="text/javascript">
let defaultCourses = network.body.data.nodes.get().filter(node => node.title === "Course");
let defaultEdges = network.body.data.edges.get().filter(edge => edge.title === "Prerequisite");

function updateCourseNodeFont() {
    // Get all course nodes
    const courseNodes = network.body.data.nodes.get().filter(node => node.title === "Course");

    // Update the font size and border properties for each course node
    const updatedCourseNodes = courseNodes.map(node => ({
        id: node.id,
        font: {
            size: 25, // Set font size to 25 (adjust as needed)
            color: 'black', // Text color
            face: 'arial', // Font face
            strokeWidth: 4, // Border width (black margin)
            strokeColor: 'white' // Border color
        },
        size: 40
    }));

    // Get all objective nodes
    const objectiveNodes = network.body.data.nodes.get().filter(node => node.title === "Objective");

    // Update the font size and border properties for each objective node
    const updatedObjectiveNodes = objectiveNodes.map(node => ({
        id: node.id,
        borderWidthSelected: 4, // Thicker when selected
        borderColor: "green", // Darker green border for emphasis
        font: {
            size: 20, // Set font size to 20 (adjust as needed)
            color: 'black', // Text color
            face: 'arial', // Font face
            strokeWidth: 2, // Border width (black margin)
            strokeColor: 'white' // Border color
        }
    }));

    // Apply the updates to the nodes in one call
    network.body.data.nodes.update([...updatedCourseNodes, ...updatedObjectiveNodes]);
}


function isLoadingComplete() {
    const loadingBar = document.getElementById('loadingBar');
    if (loadingBar) {
        // Check if the loading bar's opacity is set to 0 or width is 100% as a completion check
        return loadingBar.style.opacity === '0' || loadingBar.style.width === '100%';
    }
    return false; // Return false if the element is not found
}

// Function to disable physics when loading is complete
function disablePhysicsWhenLoaded() {
    if (isLoadingComplete()) {
        network.setOptions({
            physics: {
                enabled: false
            }
        });
    } else {
        // Wait and check again after a short delay
        setTimeout(disablePhysicsWhenLoaded, 100); // Adjust the interval as needed
    }
}


// Run when the window is loaded
window.onload = function() {
    // Wait for loading completion before disabling physics
    disablePhysicsWhenLoaded();
    updateCourseNodeFont();
};

// Add a timer to freeze the gravitational effect after 90 seconds (plan b)
/* setTimeout(() => {
    network.setOptions({
        physics: {
            enabled: false // Disable physics to prevent nodes from moving
        }
    });
}, 90000); */


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
        const isPrerequisite = edge.color === "white"; // Assuming black is used for prerequisite edges
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
resetButton.style.borderRadius = "5px";
resetButton.style.border = "2px solid white";  // White border
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


// Add a button to hide selected objective, its course, and objectives it depends on
const hideObjectiveButton = document.createElement("button");
hideObjectiveButton.innerText = "Check Requisites";

// Style the button
hideObjectiveButton.style.position = "absolute";
hideObjectiveButton.style.top = "10px";
hideObjectiveButton.style.right = "10px";
hideObjectiveButton.style.zIndex = "1000";
hideObjectiveButton.style.padding = "10px 20px";
hideObjectiveButton.style.fontSize = "16px";
hideObjectiveButton.style.backgroundColor = "#dc3545"; // Bootstrap's danger color
hideObjectiveButton.style.color = "white";
hideObjectiveButton.style.border = "2px solid white";
hideObjectiveButton.style.borderRadius = "5px";
hideObjectiveButton.style.cursor = "pointer";
hideObjectiveButton.style.transition = "background-color 0.3s, transform 0.2s";

// Hover effect
hideObjectiveButton.onmouseover = () => {
    hideObjectiveButton.style.backgroundColor = "#a71d2a"; // Darker red on hover
    hideObjectiveButton.style.transform = "scale(1.05)";
};

hideObjectiveButton.onmouseout = () => {
    hideObjectiveButton.style.backgroundColor = "#dc3545"; // Original red color
    hideObjectiveButton.style.transform = "scale(1)";
};

document.body.appendChild(hideObjectiveButton);
// Function to hide selected objective and its dependencies
hideObjectiveButton.onclick = function () {
    const selectedNodes = network.getSelectedNodes();
    if (selectedNodes.length === 0) {
        alert("Please select an objective node first.");
        return;
    }

    const selectedNodeId = selectedNodes[0];
    const selectedNode = network.body.data.nodes.get(selectedNodeId);

    if (selectedNode.title !== "Objective") {
        alert("Please select an objective node.");
        return;
    }

    const parentCourseId = selectedNodeId.split("-")[0];

    // Find all nodes this objective depends on (incoming edges)
    const incomingEdges = network.body.data.edges.get().filter(edge => edge.to === selectedNodeId);
    const dependentNodes = incomingEdges.map(edge => edge.from);

    // Hide the selected objective node, its course, and the objectives it depends on
    network.body.data.nodes.update([
        { id: selectedNodeId, hidden: false }, // Show the selected objective
        { id: parentCourseId, hidden: false }, // Show the parent course
        ...dependentNodes.map(nodeId => ({ id: nodeId, hidden: false })) // Show all nodes it depends on
    ]);

    // Ensure edges leading to visible nodes are shown
    network.body.data.edges.update(incomingEdges.map(edge => ({ id: edge.id, hidden: false })));

    // Hide prerequisite nodes, their edges, and the associated courses
    const outgoingEdges = network.body.data.edges.get().filter(edge => edge.from === selectedNodeId);
    outgoingEdges.forEach(edge => {
        const prerequisiteNodeId = edge.to;
        network.body.data.edges.update({ id: edge.id, hidden: true });
        network.body.data.nodes.update({ id: prerequisiteNodeId, hidden: true }); // Hide prerequisite nodes
        
        // Hide the course associated with the prerequisite node
        const prerequisiteNode = network.body.data.nodes.get(prerequisiteNodeId);
        if (prerequisiteNode && prerequisiteNodeId.split("-").length > 1) {
            const courseId = prerequisiteNodeId.split("-")[0];
            network.body.data.nodes.update({ id: courseId, hidden: true });
        }
    });
};

// Add a second button to show/hide the opposite elements
const showHideOppositeButton = document.createElement("button");
showHideOppositeButton.innerText = "Check Dependencies";

// Style the button
showHideOppositeButton.style.position = "absolute";
showHideOppositeButton.style.top = "50px"; // Positioned below the first button
showHideOppositeButton.style.right = "10px";
showHideOppositeButton.style.zIndex = "1000";
showHideOppositeButton.style.padding = "10px 20px";
showHideOppositeButton.style.fontSize = "16px";
showHideOppositeButton.style.backgroundColor = "#dc3545"; // Bootstrap's success color
showHideOppositeButton.style.color = "white";
showHideOppositeButton.style.border = "2px solid white";
showHideOppositeButton.style.marginTop = "10px";
showHideOppositeButton.style.borderRadius = "5px";
showHideOppositeButton.style.cursor = "pointer";
showHideOppositeButton.style.transition = "background-color 0.3s, transform 0.2s";

// Hover effect
showHideOppositeButton.onmouseover = () => {
    showHideOppositeButton.style.backgroundColor = "#a71d2a"; // Darker green on hover
    showHideOppositeButton.style.transform = "scale(1.05)";
};

showHideOppositeButton.onmouseout = () => {
    showHideOppositeButton.style.backgroundColor = "#dc3545"; // Original green color
    showHideOppositeButton.style.transform = "scale(1)";
};

document.body.appendChild(showHideOppositeButton);

// Function to show/hide the opposite of the selected objective and its dependencies
showHideOppositeButton.onclick = function () {
    const selectedNodes = network.getSelectedNodes();
    if (selectedNodes.length === 0) {
        alert("Please select an objective node first.");
        return;
    }

    const selectedNodeId = selectedNodes[0];
    const selectedNode = network.body.data.nodes.get(selectedNodeId);

    if (selectedNode.title !== "Objective") {
        alert("Please select an objective node.");
        return;
    }

    const parentCourseId = selectedNodeId.split("-")[0];

    // Find all nodes that the selected node depends on (incoming edges)
    const incomingEdges = network.body.data.edges.get().filter(edge => edge.to === selectedNodeId);
    const prerequisiteNodes = incomingEdges.map(edge => edge.from);

    // Find all nodes linked to the selected node (outgoing edges)
    const outgoingEdges = network.body.data.edges.get().filter(edge => edge.from === selectedNodeId);
    const linkedNodes = outgoingEdges.map(edge => edge.to);

    // Find the edge connecting the parent course and the selected objective
    const courseEdge = network.body.data.edges.get().find(edge => edge.from === parentCourseId && edge.to === selectedNodeId);

    // Update visibility of nodes and edges
    network.body.data.nodes.update([
        { id: selectedNodeId, hidden: false }, // Show the selected objective
        { id: parentCourseId, hidden: false }, // Show the parent course
        ...prerequisiteNodes.map(nodeId => ({ id: nodeId, hidden: true })), // Hide prerequisite nodes
        ...linkedNodes.map(nodeId => ({ id: nodeId, hidden: false })) // Show nodes linked to the selected objective
    ]);

    network.body.data.edges.update([
        ...incomingEdges.map(edge => ({ id: edge.id, hidden: true })), // Hide incoming edges
        ...outgoingEdges.map(edge => ({ id: edge.id, hidden: false })), // Show outgoing edges
        courseEdge ? { id: courseEdge.id, hidden: false } : null // Ensure course-objective edge is shown
    ].filter(Boolean)); // Remove null entries

    // Ensure associated courses for prerequisites are hidden
    prerequisiteNodes.forEach(prerequisiteNodeId => {
        const prerequisiteNode = network.body.data.nodes.get(prerequisiteNodeId);
        if (prerequisiteNode && prerequisiteNodeId.split("-").length > 1) {
            const courseId = prerequisiteNodeId.split("-")[0];
            network.body.data.nodes.update({ id: courseId, hidden: true });
        }
    });

    // Ensure associated courses for linked nodes are shown
    linkedNodes.forEach(linkedNodeId => {
        const linkedNode = network.body.data.nodes.get(linkedNodeId);
        if (linkedNode && linkedNodeId.split("-").length > 1) {
            const courseId = linkedNodeId.split("-")[0];
            network.body.data.nodes.update({ id: courseId, hidden: false });
        }
    });

    // Ensure the course of the selected node is always shown
    network.body.data.nodes.update({ id: parentCourseId, hidden: false });
};

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

// Search input field for dark mode
searchInput.style.backgroundColor = "#2b2b2b";  // Dark background
searchInput.style.color = "white";  // White text
searchInput.style.border = "2px solid white";  // White border

// Suggestions container for dark mode
suggestionsContainer.style.backgroundColor = "#333";  // Darker background
suggestionsContainer.style.color = "white";  // White text
suggestionsContainer.style.border = "1px solid white";  // White border

</script>
"""

# Inject JavaScript into the HTML
html_content += custom_js

# Save the modified HTML file
with open(output_file, "w", encoding="utf-8") as file:
    file.write(html_content)

print(f"Graph saved as {output_file}")
