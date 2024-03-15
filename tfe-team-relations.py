import argparse
import requests
from prettytable import PrettyTable
from __setup import tfe_setup

# Setup auth etc
organization, base_url, headers = tfe_setup()

def get_teams():
    url = f"{base_url}/teams"
    print(f'Accessing: {url}')
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    if 'data' not in data:
        print(f'Error: No data in response: {data}')
        exit(1)
    return data

def main():
    teams = get_teams()

    table = PrettyTable()
    table.field_names = ["Team ID", "Team Name", "Project ID", "Project Name"]

    for team in teams['data']:
        team_id = team['id']
        team_name = team['attributes']['name']
        team_access_url = f"{base_url}/teams/{team_id}/access"
        team_access_response = requests.get(team_access_url, headers=headers)
        team_access = team_access_response.json().get('data', [])

        for project in team_access:
            project_id = project['id']
            project_name = project['attributes']['name']
            table.add_row([team_id, team_name, project_id, project_name])

    print(table)

if __name__ == "__main__":
    main()