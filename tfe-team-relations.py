import requests
from prettytable import PrettyTable
from __setup import tfe_setup

# Setup auth etc
organization, base_url, headers = tfe_setup()

def get_workspaces():
    url = f"{base_url}/organizations/{organization}/workspaces"
    workspaces = []

    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if 'data' not in data:
            print(f'Error: No data in response: {data}')
            exit(1)
        workspaces.extend(data['data'])

        # Get the next page URL, if it exists
        url = data['links'].get('next', None)

    return workspaces

def get_team_access():
    workspace = get_workspaces()
    url = f"{base_url}/team-workspaces?filter%5Bworkspace%5D%5Bid%5D={workspace['id']}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    if 'data' not in data:
        print(f'Error: No data in response: {data}')
        exit(1)
    return data

def main():
    workspaces = get_workspaces()

    table = PrettyTable()
    table.field_names = ["Team ID", "Team Name", "Workspace ID", "Workspace Name"]

    for workspace in workspaces:
        teams = get_team_access(workspace['id'])

        for team in teams['data']:
            if 'id' in team:
                team_id = team['id']
                team_name = team['attributes']['name']
                workspace_id = workspace['id']
                workspace_name = workspace['attributes']['name']
                table.add_row([team_id, team_name, workspace_id, workspace_name])

    print(table)

if __name__ == "__main__":
    main()