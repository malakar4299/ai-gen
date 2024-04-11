import requests
import csv
import json
from dotenv import load_dotenv
import os
import base64
import time
import argparse

# Load environment variables from .env file
load_dotenv()

# Get the GitHub token from .env file
GITHUB_TOKEN = os.getenv("git_token")

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"token {GITHUB_TOKEN}" if GITHUB_TOKEN else None
}

topic_headers = headers.copy()  # Make a copy of the existing headers
topic_headers["Accept"] = "application/vnd.github.mercy-preview+json"  # Modify or add the specific header


# organizations = ["microsoft"]  # Example organizations , "google-research", "microsoft", "apple", "facebookresearch", "amazon-science", "google-deepmind"

def get_arguments():
    parser = argparse.ArgumentParser(description='Fetch GitHub repository data for specified organizations.')
    parser.add_argument('--orgs', type=str, help='Path to a text file containing organization names, one per line.', required=True)
    args = parser.parse_args()
    return args

def get_response_with_rate_limit(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 403 and 'X-RateLimit-Remaining' in response.headers and response.headers['X-RateLimit-Remaining'] == '0':
        reset_time = float(response.headers['X-RateLimit-Reset'])
        sleep_time = reset_time - time.time() + 10  # Adding a 10 second buffer
        print(f"Rate limit exceeded. Waiting for {sleep_time} seconds.")
        time.sleep(sleep_time)
        return get_response_with_rate_limit(url, headers)  # Retry the request
    return response

def get_repos(org):
    print("Fetching Repo's")
    """Fetch all repositories for a given organization."""
    repos = []
    page = 0
    while True:
        url = f"https://api.github.com/users/{org}/repos?page={page}&per_page=100"
        response = get_response_with_rate_limit(url, headers=headers)
        data = response.json()
        # print(response)
        if not data or response.status_code != 200:
            break
        repos.extend(data)
        page += 1

    print("Repos fetched")
    return repos

def get_repo_metadata(org, repo_name):
    """Fetch metadata for a specific repository."""
    repo_info = get_response_with_rate_limit(f"https://api.github.com/repos/{org}/{repo_name}", headers=headers).json()
    readme_info = get_response_with_rate_limit(f"https://api.github.com/repos/{org}/{repo_name}/readme", headers=headers).json()
    topics_info = get_response_with_rate_limit(f"https://api.github.com/repos/{org}/{repo_name}/topics", headers=topic_headers).json()
    
    # Decode README content from Base64
    readme_content = ""
    if readme_info.get('content'):
        readme_content = base64.b64decode(readme_info['content']).decode('utf-8')
    
    return {
        "repo_info": repo_info,
        "readme": readme_content,
        "topics": topics_info.get("names", [])
    }

def save_to_csv(data, filename="repo_summary.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Organization", "Repo Name", "Stars", "Forks", "Primary Language", "Topics"])
        for item in data:
            writer.writerow([item['Organization'], item['Repo Name'], item['Stars'], item['Forks'], item['Primary Language'], ";".join(item['Topics'])])

def save_to_json(data, filename="repo_details.json"):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def append_to_csv(repos, filename="repo_summary_new.csv"):
    print(f"Appending {len(repos)} repositories to {filename}...")
    # Check if the file exists to write headers only once
    file_exists = os.path.isfile(filename)
    
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Organization", "Repo Name", "Stars", "Forks", "Primary Language", "Topics"])
        for repo in repos:
            writer.writerow([repo['Organization'], repo['Repo Name'], repo['Stars'], repo['Forks'], repo['Primary Language'], ";".join(repo['Topics'])])

    print("CSV append operation completed.")

def append_to_json(data, filename="repo_details_new.json"):
    print(f"Appending data to {filename}...")
    existing_data = []
    if os.path.isfile(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = []

    # Append the new data (ensure that data is a list before appending)
    existing_data.extend(data if isinstance(data, list) else [data])
    
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)

    print("JSON append operation completed.")

def main():
    args = get_arguments()
    orgs_file_path = args.orgs
    # Default organization list to fall back on
    default_organizations = ["microsoft", "google-research", "apple", "facebookresearch", "amazon-science", "google-deepmind"]
    organizations = []

    if orgs_file_path and os.path.exists(orgs_file_path):
        # Read organization names from the text file if it exists
        with open(orgs_file_path, 'r') as file:
            organizations = [line.strip() for line in file if line.strip()]
    else:
        # Fall back to the default list if the file does not exist or is not specified
        organizations = default_organizations
                 
    repo_summary = []
    repo_details = []

    for org in organizations:
        repos = get_repos(org)
        for repo in repos:
            metadata = get_repo_metadata(org, repo['name'])
            repo_summary.append({
                "Organization": org,
                "Repo Name": repo['name'],
                "Stars": repo['stargazers_count'],
                "Forks": repo['forks_count'],
                "Primary Language": repo['language'],
                "Topics": metadata['topics']
            })
            repo_details.append(metadata)  # Assuming you want the whole repo info here

    append_to_csv(repo_summary)
    append_to_json(repo_details)

if __name__ == "__main__":
    main()
