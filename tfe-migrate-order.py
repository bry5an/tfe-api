import pandas as pd
import networkx as nx

# Step 1: Read the Excel file
df = pd.read_excel('workspaces.xlsx')

# Step 2: Create a directed graph
G = nx.DiGraph()

# Add nodes
for index, row in df.iterrows():
    G.add_node(row['WorkspaceName'])

# Add edges based on remote workspaces
for index, row in df.iterrows():
    if pd.notna(row['RemoteWorkspace']):
        remote_workspaces = row['RemoteWorkspace'].split(',')
        for remote_workspace in remote_workspaces:
            G.add_edge(remote_workspace.strip(), row['WorkspaceName'])

# Step 3: Detect cycles and assign unique values
cycles = list(nx.simple_cycles(G))
cycle_workspaces = set()
cycle_order_dict = {}

for i, cycle in enumerate(cycles):
    for workspace in cycle:
        cycle_workspaces.add(workspace)
        cycle_order_dict[workspace] = f'cycle-{i+1}'

# Remove cycle workspaces from the graph
G.remove_nodes_from(cycle_workspaces)

# Step 4: Calculate the depth of each workspace
depth_dict = {}
for node in nx.topological_sort(G):
    predecessors = list(G.predecessors(node))
    if not predecessors:
        depth_dict[node] = 0
    else:
        depth_dict[node] = max(depth_dict[pred] for pred in predecessors) + 1

# Assign group numbers based on depth
group_dict = {workspace: depth + 1 for workspace, depth in depth_dict.items()}

# Combine the two dictionaries
group_dict.update(cycle_order_dict)

# Step 5: Add the group number to the DataFrame
df['MigrationGroup'] = df['WorkspaceName'].map(group_dict)

# Save the updated DataFrame back to the Excel file
df.to_excel('workspaces_with_group.xlsx', index=False)

print("Migration groups have been added to the Excel file.")