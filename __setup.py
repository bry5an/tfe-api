import argparse
import os

def tfe_setup():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--organization', help='The name of the organization to query.')
    parser.add_argument("--tfe", action='store_true')
    parser.add_argument("--tfc", action='store_true')
    args = parser.parse_args()

    if args.tfe:
        tf_url = "tfe.com"
    elif args.tfc:
        tf_url = "app.terraform.io"
    else:
        print("Error: Please specify either --tfe or --tfc.")
        exit(1)

    organization = args.organization
    base_url = f'https://{tf_url}/api/v2/organizations/{organization}'
    headers = {"Authorization": f"Bearer {os.getenv('TFE_TOKEN')}"}

    # if 'TFE_TOKEN' not in os.getenv:
    #     print("Error: The TFE_TOKEN environment variable is not set. Please export it before running the script.")
    #     exit(1)

    return organization, base_url, headers