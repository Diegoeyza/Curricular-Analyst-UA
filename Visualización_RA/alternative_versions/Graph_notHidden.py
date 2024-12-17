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

# Add courses as nodes from the General sheet
for _, row in general_df.iterrows():
    course_id = row['ID']
    course_name = row['Nombre']
    graph.add_node(course_id, label=course_name, type="course")

# Add prerequisites as edges from the Requirements sheet
for _, row in requirements_df.iterrows():
    course_id = row['ID']
    prereq_id = row['ID_Requisito']
    graph.add_edge(prereq_id, course_id, type="prerequisite")

# Add course objectives as nodes from the Objectives sheet
for _, row in objectives_df.iterrows():
    course_id = row['ID']
    objective_id = row['ID_Objetivo']
    objective_name = row['Objetivo']
    node_label = f"{course_id}-{objective_id}"
    graph.add_node(node_label, label=objective_name, type="objective")
    graph.add_edge(course_id, node_label, type="has_objective")

# Add objective links as edges from the RA_Links sheet
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

# Add nodes and edges with attributes to the Pyvis network
for node, data in graph.nodes(data=True):
    node_type = data.get("type", "unknown")
    label = data.get("label", str(node))
    if node_type == "course":
        net.add_node(node, label=label, color="lightblue", title="Course")
    elif node_type == "objective":
        net.add_node(node, label=label, color="lightgreen", title="Objective", hidden=True)
    else:
        net.add_node(node, label=label, color="grey", title="Unknown")

for source, target, data in graph.edges(data=True):
    edge_type = data.get("type", "unknown")
    importancia = data.get("importancia", "")
    if edge_type == "prerequisite":
        net.add_edge(source, target, color="red", title="Prerequisite")
    elif edge_type == "has_objective":
        net.add_edge(source, target, color="black", title="Has Objective")
    elif edge_type == "objective_link":
        net.add_edge(source, target, color="blue", title=importancia, label=importancia, hidden=True)
    else:
        net.add_edge(source, target, color="grey", title="Unknown")

# Set basic JSON options for physics and interaction
net.set_options("""
{
  "interaction": {
    "hover": true
  },
  "physics": {
    "barnesHut": {
      "gravitationalConstant": -20000,
      "centralGravity": 0.3,
      "springLength": 95,
      "springConstant": 0.04,
      "damping": 0.09
    },
    "minVelocity": 0.75
  }
}
""")

# Save and display the graph
output_file = "curricular_graph.html"
net.save_graph(output_file)

# Add custom JavaScript to the HTML
with open(output_file, "r", encoding="utf-8") as file:
    html_content = file.read()

custom_js = """
<script type="text/javascript">
let defaultState = network.body.data.nodes.get({
    returnType: "Object"
});

document.querySelector("button#reset").addEventListener("click", function () {
    network.body.data.nodes.update(Object.values(defaultState));
    network.body.data.edges.update(Object.values(defaultEdges));
});

network.on("click", function (params) {
    if (params.nodes.length > 0) {
        let clickedNode = params.nodes[0];
        let connectedNodes = network.getConnectedNodes(clickedNode);
        let connectedEdges = network.getConnectedEdges(clickedNode);
        network.body.data.nodes.update({ id: clickedNode, hidden: false });
    }
});
</script>
"""

# Insert the custom JavaScript before the closing </body> tag
html_content = html_content.replace("</body>", custom_js + "</body>")

# Save the updated HTML file
with open(output_file, "w", encoding="utf-8") as file:
    file.write(html_content)

print(f"Interactive graph with custom events saved to {output_file}")
