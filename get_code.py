import requests
import time
import argparse
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the GitHub token from .env file
GITHUB_TOKEN = os.getenv("git_token")

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"token {GITHUB_TOKEN}" if GITHUB_TOKEN else None
}

def list_files_in_repo(owner, repo, path):
    """
    List all files in a GitHub repository at a specified path.

    Parameters:
    - owner: The owner of the repository.
    - repo: The name of the repository.
    - path: The directory path to list files from. Use "" for root.
    - token: Your GitHub Personal Access Token for authentication.

    Returns:
    A list of file paths within the specified directory.
    """
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    response = get_response_with_rate_limit(api_url, headers=headers)
    files = []

    if response.status_code == 200:
        contents = response.json()
        for item in contents:
            if item['type'] == 'file':
                files.append(item['path'])
            elif item['type'] == 'dir':
                files.extend(list_files_in_repo(owner, repo, item['path']))
    else:
        print("Failed to list files:", response.status_code)

    return files

def fetch_repo_code_files(owner, repo):
    """
    Fetch all code files from a GitHub repository and store them in a dictionary.

    Parameters:
    - owner: The owner of the repository.
    - repo: The name of the repository.
    - token: GitHub Personal Access Token for authentication.

    Returns:
    A dictionary with file paths as keys and file contents as values.
    """
    file_paths = list_files_in_repo(owner, repo, "")
    code_files = {}

    for path in file_paths:
        content = fetch_file_contents(owner, repo, path)
        if content:  # Ensure only successful fetches are added
            code_files[path] = content

    return code_files

def get_arguments():
    parser = argparse.ArgumentParser(description='Fetch GitHub repository data for specified organizations.')
    parser.add_argument('--orgs', type=str, help='Path to a text file containing organization names, one per line.', required=True)
    args = parser.parse_args()
    return args

topic_headers = headers.copy()  # Make a copy of the existing headers
topic_headers["Accept"] = "application/vnd.github.mercy-preview+json"  # Modify or add the specific header

def get_response_with_rate_limit(url, headers=headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 403 and 'X-RateLimit-Remaining' in response.headers and response.headers['X-RateLimit-Remaining'] == '0':
        reset_time = float(response.headers['X-RateLimit-Reset'])
        sleep_time = reset_time - time.time() + 10  # Adding a 10 second buffer
        print(f"Rate limit exceeded. Waiting for {sleep_time} seconds.")
        time.sleep(sleep_time)
        return get_response_with_rate_limit(url, headers)  # Retry the request
    return response

def fetch_file_contents(owner, repo, file_path):
    """
    Fetch the contents of a file from a GitHub repository.

    Parameters:
    - owner: The owner of the repository.
    - repo: The name of the repository.
    - file_path: The path to the file within the repository.
    - token: Your GitHub Personal Access Token for authentication.

    Returns:
    The contents of the file as a string.
    """
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    response = get_response_with_rate_limit(api_url, headers=headers)
    if response.status_code == 200:
        file_content = response.json()
        print(get_response_with_rate_limit(file_content['download_url']).text)
    else:
        print("Failed to fetch file contents:", response.status_code)
        return None
    

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

    for org in organizations:
        repos = get_repos(org)
        repo = repos[0]['name']

        print(repo)

        code_files = fetch_repo_code_files(org, repo)

        print(code_files)



if __name__ == "__main__":
    main()