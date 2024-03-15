import argparse
import requests
from prettytable import PrettyTable
from __setup import tfe_setup

organization, base_url = tfe_setup()

def get_teams(organization):
    response = requests.get(f'{base_url}/teams')
    return response.json()

def get_projects(organization, team):
    response = requests.get(f'{base_url}/teams/{team}/relationships/workspaces')
    return response.json()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('organization')
    args = parser.parse_args()

    teams = get_teams(organization)

    table = PrettyTable()
    table.field_names = ["Team", "Project"]

    for team in teams['data']:
        projects = get_projects(organization, team['id'])
        for project in projects['data']:
            table.add_row([team['attributes']['name'], project['attributes']['name']])

    print(table)

if __name__ == "__main__":
    main()