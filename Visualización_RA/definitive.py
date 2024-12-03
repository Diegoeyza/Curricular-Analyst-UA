import pandas as pd
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
    node_label = f"{course_id}-{objective_id}"
    graph.add_node(node_label, label=objective_name, type="objective")
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
        net.add_node(node, label=label, color="lightblue", title="Course")
    elif node_type == "objective":
        net.add_node(node, label=label, color="lightgreen", title="Objective", hidden=True)  # Initially hidden
    else:
        net.add_node(node, label=label, color="grey", title="Unknown", hidden=True)

for source, target, data in graph.edges(data=True):
    edge_type = data.get("type", "unknown")
    importancia = data.get("importancia", "")
    net.add_edge(source, target, color="blue", title=importancia, label=importancia)

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
    "minVelocity": 0.75
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
    network.body.data.nodes.update(defaultCourses.map(node => ({ id: node.id, hidden: false })));
    
    // Show all prerequisite edges
    network.body.data.edges.update(defaultEdges.map(edge => ({ id: edge.id, hidden: false })));

    // Ensure objectives remain hidden
    let objectives = network.body.data.nodes.get().filter(node => node.title === "Objective");
    network.body.data.nodes.update(objectives.map(node => ({ id: node.id, hidden: true })));
}

// Add a reset button
const resetButton = document.createElement("button");
resetButton.innerText = "Reset View";
resetButton.style.position = "absolute";
resetButton.style.top = "10px";
resetButton.style.left = "10px";
resetButton.style.zIndex = "1000";
resetButton.onclick = resetView;
document.body.appendChild(resetButton);

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

            // Find linked objectives and their courses
            let linkedEdges = network.body.data.edges.get().filter(edge =>
                edge.from === objectiveId || edge.to === objectiveId
            );
            let linkedNodes = new Set(linkedEdges.flatMap(edge => [edge.from, edge.to]));

            // Ensure linked objectives and their courses are visible
            let nodesToShow = network.body.data.nodes.get().filter(node =>
                linkedNodes.has(node.id) || (node.title === "Course" && linkedNodes.has(node.id))
            );

            // Add the course linked to the clicked objective
            let parentCourse = network.body.data.nodes.get().find(node =>
                node.title === "Course" && objectiveId.startsWith(node.id + "-")
            );
            if (parentCourse) {
                nodesToShow.push(parentCourse);
            }

            // Add courses related to linked objectives
            linkedNodes.forEach(linkedNodeId => {
                let relatedCourse = network.body.data.nodes.get().find(node =>
                    node.title === "Course" && linkedNodeId.startsWith(node.id + "-")
                );
                if (relatedCourse) {
                    nodesToShow.push(relatedCourse);
                }
            });

            // Hide everything else
            network.body.data.nodes.update(network.body.data.nodes.get().map(node => ({
                id: node.id,
                hidden: !nodesToShow.some(n => n.id === node.id),
            })));

            // Update edges to show only the relevant ones
            network.body.data.edges.update(defaultEdges.map(edge => ({
                id: edge.id,
                hidden: !linkedEdges.some(e => e.id === edge.id),
            })));
        }
    }
});
</script>

"""

# Inject custom JavaScript into the HTML
html_content = html_content.replace("</body>", custom_js + "</body>")

# Save the updated HTML file
with open(output_file, "w", encoding="utf-8") as file:
    file.write(html_content)

print(f"Interactive graph with custom interactivity saved to {output_file}")
