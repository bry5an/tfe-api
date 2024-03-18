import requests
from prettytable import PrettyTable
from __setup import tfe_setup

# Setup auth etc
organization, base_url, headers = tfe_setup()

def get_all_projects():
    url = f"{base_url}/api/v2/organizations/{organization}/projects"
    projects = []
    while url:
        response = requests.get(url, headers=headers)
        data = response.json()
        projects.extend(data['data'])
        url = data['links'].get('next')  # Get the next page URL
    return projects

def get_project_team_access(project_id):
    url = f"{base_url}/api/v2/projects/{project_id}/team-access"
    response = requests.get(url, headers=headers)
    data = response.json()
    return data['data']

def list_project_team_associations():
    projects = get_all_projects()
    table = PrettyTable()
    table.field_names = ["Project ID", "Project Name", "Team ID", "Team Name"]
    for project in projects:
        project_id = project['id']
        project_name = project['attributes']['name']
        team_accesses = get_project_team_access(project_id)
        for team_access in team_accesses:
            team_id = team_access['relationships']['team']['data']['id']
            team_name = team_access['attributes']['name']
            table.add_row([project_id, project_name, team_id, team_name])
    print(table)

list_project_team_associations()