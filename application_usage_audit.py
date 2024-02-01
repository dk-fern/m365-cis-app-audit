import msal
import os
import requests
from typing import List

# Authenticate with Microsoft and return access token
def graph_api_authentication() -> str:    
    try:
        # Define Credentials
        CLIENT_ID = os.environ['CLIENT_ID']
        TENANT_ID = os.environ['TENANT_ID']
        THUMBPRINT = os.environ['THUMBPRINT']
        AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'  
        
        CERT = {'thumbprint': THUMBPRINT,
                'private_key': open(r'<Path to your .key file>').read()
                }

        # Begin authentication with Graph api
        app = msal.ConfidentialClientApplication(
            client_id=CLIENT_ID,
            authority=AUTHORITY,
            client_credential=CERT
            )
        SCOPE = ["https://graph.microsoft.com/.default"]

        # Determine if authentication was successful
        result = app.acquire_token_silent(SCOPE, account=None)
        if not result:
            result = app.acquire_token_for_client(scopes=SCOPE)

        # --------------ACCESS TOKEN -----------------#
        if "access_token" in result:
            access_token = result["access_token"]
        #---------------------------------------------#

        else:
            print(result.get("error"))
            print(result.get("error_description"))

    except Exception as e:
        print(f"Error: {str(e)}")

    return access_token

# Use access token to look up applications usage from the last week in the tenant
def azure_lookup(access_token :str) -> List:    
    try:
        # Define endpoint, headers variables
        graph_endpoint = "https://graph.microsoft.com/beta/reports/getAzureADApplicationSignInSummary(period='D7')"
        headers = {
            'Authorization': f'Bearer {access_token}',
        }
        response = requests.get(graph_endpoint, headers=headers)

        # Error check for other status code than 200
        if response.status_code == 200:
            data = response.json()
            value = data.get('value', [])
            
            # Use list comprehension to loop over returned data and write it to apps list
            apps = [item['appDisplayName'] for item in value]

        else:
            return(f"Error:{response.text}")

        # Return list of applications used in the last month
        return apps

    except Exception as e:
        print(f"Error: {str(e)}")

# Take returned list of used applications and compare with baseline applications list.
# Returns list of applications that need to be looked into
def compare_to_baseline(apps_list :List) -> List:
    from baseline_applications import BASELINE_APPLICATIONS
    apps_to_investigate = [app for app in apps_list if app not in BASELINE_APPLICATIONS]
    return apps_to_investigate

# Run all functions and print apps to investigate to the console
def main():
    access_token = graph_api_authentication()
    app_list = azure_lookup(access_token)
    apps_to_investigate = compare_to_baseline(app_list)
    for app in apps_to_investigate:
        print(app)

if __name__ == '__main__':
    main()