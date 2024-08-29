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

# Step 4: Perform topological sort on the remaining graph
try:
    migration_order = list(nx.topological_sort(G))
except nx.NetworkXUnfeasible:
    print("Error: The graph still has cycles after removing detected cycles.")
    exit(1)

# Create a dictionary to map workspace names to their migration order
order_dict = {workspace: order for order, workspace in enumerate(migration_order)}

# Combine the two dictionaries
order_dict.update(cycle_order_dict)

# Step 5: Add the migration order to the DataFrame
df['MigrationOrder'] = df['WorkspaceName'].map(order_dict)

# Save the updated DataFrame back to the Excel file
df.to_excel('workspaces_with_order.xlsx', index=False)

print("Migration order has been added to the Excel file.")