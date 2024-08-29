import pandas as pd
import networkx as nx
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

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

# Step 6: Highlight remote workspace names
wb = load_workbook('workspaces_with_group.xlsx')
ws = wb.active

highlight_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")

for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
    for cell in row:
        if cell.column_letter == 'C' and cell.value:  # Assuming 'RemoteWorkspace' is in column C
            remote_workspaces = cell.value.split(',')
            for remote_workspace in remote_workspaces:
                remote_workspace = remote_workspace.strip()
                for r in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
                    for c in r:
                        if c.value == remote_workspace:
                            c.fill = highlight_fill

wb.save('workspaces_with_group_highlighted.xlsx')

print("Migration groups and highlights have been added to the Excel file.")# Step 4: Calculate the depth of each workspace
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

# Step 6: Highlight remote workspace names
wb = load_workbook('workspaces_with_group.xlsx')
ws = wb.active

highlight_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")

for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
    for cell in row:
        if cell.column_letter == 'C' and isinstance(cell.value, str):  # Check if cell value is a string
            remote_workspaces = cell.value.split(',')
            for remote_workspace in remote_workspaces:
                remote_workspace = remote_workspace.strip()
                for r in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
                    for c in r:
                        if c.value == remote_workspace:
                            c.fill = highlight_fill

wb.save('workspaces_with_group_highlighted.xlsx')

print("Migration groups and highlights have been added to the Excel file.")