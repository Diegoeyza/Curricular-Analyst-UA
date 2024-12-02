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
    # Link course to its objectives
    graph.add_edge(course_id, node_label, type="has_objective")

# Add objective links as edges from the RA_Links sheet
for _, row in ra_links_df.iterrows():
    course_id = row['ID']
    objective_id = row['ID_Objetivo']
    linked_course_id = row['ID_Prerequisito']
    linked_objective_id = row['ID_Objetivo_Prerrequisito']
    source_node = f"{course_id}-{objective_id}"
    target_node = f"{linked_course_id}-{linked_objective_id}"
    graph.add_edge(source_node, target_node, type="objective_link")

# Create an interactive Pyvis network
net = Network(height="1000px", width="100%", directed=True)

# Add nodes and edges with attributes to the Pyvis network
for node, data in graph.nodes(data=True):
    node_type = data.get("type", "unknown")
    label = data.get("label", str(node))  # Default to node ID if no label exists
    if node_type == "course":
        net.add_node(node, label=label, color="lightblue", title="Course")
    elif node_type == "objective":
        net.add_node(node, label=label, color="lightgreen", title="Objective")
    else:
        net.add_node(node, label=label, color="grey", title="Unknown")

for source, target, data in graph.edges(data=True):
    edge_type = data.get("type", "unknown")
    if edge_type == "prerequisite":
        net.add_edge(source, target, color="red", title="Prerequisite")
    elif edge_type == "has_objective":
        net.add_edge(source, target, color="black", title="Has Objective")
    elif edge_type == "objective_link":
        net.add_edge(source, target, color="blue", title="Objective Link")
    else:
        net.add_edge(source, target, color="grey", title="Unknown")

# Enable clustering by course to hide objectives initially
for course_id in general_df['ID']:
    cluster_nodes = [node for node in graph.nodes if node.startswith(f"{course_id}-")]
    if cluster_nodes:
        net.add_node(course_id, label=graph.nodes[course_id]['label'], color="lightblue", title="Course", shape="dot")
        net.add_edges([(course_id, obj) for obj in cluster_nodes])

# Set physics options for better layout
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
  }
}
""")

# Save and display the graph
output_file = "curricular_graph.html"
net.save_graph(output_file)
print(f"Graph saved as: {output_file}")
print(f"Interactive graph saved to {output_file}")
