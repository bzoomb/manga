import requests
import time
from datetime import datetime

# GitHub API configuration
GITHUB_API_URL = "https://api.github.com"
REPO_OWNER = "bzoomb"
REPO_NAME = "manga"
WORKFLOW_ID = "main.yml"  # Replace with your actual workflow file name

# Define your GitHub token as a variable
GITHUB_TOKEN = ""  # Replace with your actual token

# Headers for GitHub API requests
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def start_workflow(single_index=None, index_range=None, custom_url=None):
    url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/{WORKFLOW_ID}/dispatches"
    
    inputs = {}
    if single_index:
        inputs["single_index"] = str(single_index)
    elif index_range:
        inputs["index_range"] = index_range
    elif custom_url:
        inputs["custom_url"] = custom_url
    
    data = {
        "ref": "main",  # Replace with your default branch if different
        "inputs": inputs
    }
    
    response = requests.post(url, json=data, headers=HEADERS)
    if response.status_code == 204:
        print("Workflow started successfully!")
        return True
    else:
        print(f"Failed to start workflow. Status code: {response.status_code}")
        print(response.text)
        return False

def get_workflow_runs():
    url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/{WORKFLOW_ID}/runs"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        runs = response.json().get("workflow_runs", [])
        if not runs:
            print("No workflow runs found.")
        return runs
    else:
        print(f"Failed to get workflow runs. Status code: {response.status_code}")
        print(response.text)
        return None

def monitor_workflow(run_id):
    while True:
        url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs/{run_id}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            run_data = response.json()
            status = run_data["status"]
            conclusion = run_data["conclusion"]
            
            print(f"Status: {status}, Conclusion: {conclusion}")
            
            if status == "completed":
                return conclusion
        else:
            print(f"Failed to get run status. Status code: {response.status_code}")
        
        time.sleep(30)  # Check every 30 seconds

def main():
    while True:
        print("\nManga Downloader Workflow Interaction")
        print("1. Start workflow")
        print("2. List recent workflow runs")
        print("3. Monitor a specific workflow run")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == "1":
            print("\nStart workflow:")
            print("1. Single index")
            print("2. Index range")
            print("3. Custom URL")
            start_choice = input("Enter your choice (1-3): ")
            
            if start_choice == "1":
                single_index = input("Enter single index: ")
                start_workflow(single_index=single_index)
            elif start_choice == "2":
                index_range = input("Enter index range (e.g., 3-13): ")
                start_workflow(index_range=index_range)
            elif start_choice == "3":
                custom_url = input("Enter custom URL: ")
                start_workflow(custom_url=custom_url)
            else:
                print("Invalid choice.")
        
        elif choice == "2":
            runs = get_workflow_runs()
            if runs:
                for run in runs[:5]:  # Show last 5 runs
                    started_at = datetime.strptime(run["created_at"], "%Y-%m-%dT%H:%M:%SZ")
                    print(f"Run ID: {run['id']}, Status: {run['status']}, Conclusion: {run['conclusion']}, Started: {started_at}")
            else:
                print("No workflow runs available.")
        
        elif choice == "3":
            run_id = input("Enter the run ID to monitor: ")
            result = monitor_workflow(run_id)
            print(f"Workflow completed with result: {result}")
        
        elif choice == "4":
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
