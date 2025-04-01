import requests
import json
import time
from requests.auth import HTTPBasicAuth
from tabulate import tabulate
from datetime import datetime

# Disable SSL warnings (not recommended for production)
requests.packages.urllib3.disable_warnings()

# Base configuration
DNAC_HOST = "<CatC IP address>"  # Replace with your Catalyst Center IP or hostname
DNAC_USERNAME = "<username>"        # Replace with your username
DNAC_PASSWORD = "password"        # Replace with your password
BASE_URL = f"https://{DNAC_HOST}"



# Function to get authentication token
def get_auth_token():
    url = f"{BASE_URL}/dna/system/api/v1/auth/token"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, auth=HTTPBasicAuth(DNAC_USERNAME, DNAC_PASSWORD), 
                            headers=headers, verify=False)
    response.raise_for_status()  # Raise an error if the request fails
    return response.json()["Token"]

# Backup endpoint
BACKUP_ENDPOINT = f"{BASE_URL}/api/system/v1/maglev/backup"
TASK_ENDPOINT = f"{BASE_URL}/api/v1/task"



def list_backups(token):
    """List available backups (assumes GET on the same endpoint)."""
    HEADERS = {
    "X-Auth-Token": token,
    "Content-Type": "application/json",
    "Accept": "application/json"
}
    # Note: Exact endpoint for listing might differ; adjust if needed
    response = requests.get(BACKUP_ENDPOINT, headers=HEADERS, verify=False)
    if response.status_code == 200:
        backups = response.json()
        #print("Available Backups:")
        #print(json.dumps(backups, indent=2))
        return backups
    else:
        print(f"Failed to list backups: {response.status_code} - {response.text}")
        return None



def delete_backup(token, backup_id):
    """Delete a specific backup."""
    HEADERS = {
    "X-Auth-Token": token,
    "Content-Type": "application/json",
    "Accept": "application/json"
}
    # Note: DELETE might use a sub-resource, e.g., /backup/{backupId}
    delete_endpoint = f"{BACKUP_ENDPOINT}/{backup_id}"
    response = requests.delete(delete_endpoint, headers=HEADERS, verify=False)
    if response.status_code == 200:
        print(f"Backup {backup_id} deleted successfully.")
    else:
        print(f"Failed to delete backup: {response.status_code} - {response.text}")

def main():
    retention = 4 # Number of backups to retain
    #get token
    token = get_auth_token()
    print("Authentication successful. Token retrieved.")

  

    # List backups
    print("\nListing backups...")
    backups = list_backups(token)
    
    backup_ids = []
    creation_times = []

    # Step 1: Extract backup_id and start_timestamp into a list of dictionaries
    backup_info = []
    for item in backups["response"]:
        backup_dict = {
            "backup_id": item["backup_id"],
            "start_timestamp": item["start_timestamp"],
            "creation_time": datetime.fromtimestamp(item["start_timestamp"]).strftime('%Y-%m-%d %H:%M:%S.%f')
        }
        backup_info.append(backup_dict)

    # Step 2: Sort by start_timestamp
    backup_info_sorted = sorted(backup_info, key=lambda x: x["start_timestamp"])
    print("All Backups (sorted by creation time:)")
    for backup in backup_info_sorted:
        print(f"Backup ID: {backup['backup_id']}, Start Timestamp: {backup['start_timestamp']}")
        

    # Step 3: Keep only the last {retention} (most recent)
    latest_backups = backup_info_sorted[-retention:]

    # Print the results
    print(f"Last {retention} Backups (sorted by creation time):")
    for backup in latest_backups:
        print(f"Backup ID: {backup['backup_id']}, Created: {backup['creation_time']}")
    
    
   # Check if there are more than {retention} items, and exclude the last {retention}
    if len(backup_info_sorted) > retention:
        older_backups = backup_info_sorted[:-retention]
        print(f"All Backup IDs except the last {retention}:")
        for backup in older_backups:
            #print(backup["backup_id"])
            #     # Delete a backup
            print(f"\nDeleting backup {backup["backup_id"]}, {backup['creation_time']}...")
            #delete_backup(token, backup["backup_id"])
    else:
        print(f"There are {retention} or fewer backups, so nothing to print excluding the last {retention}.")
        
    
    
 

if __name__ == "__main__":
    main()
