Certainly, here's the full markdown code for the README.md as described:

```markdown
# GitHub Repository Data Collector

This Python application (`main.py`) automates the process of collecting data from GitHub repositories for specified organizations and saves the information into CSV and JSON files. It utilizes the GitHub API and requires a GitHub token for authentication.

## Setup Instructions

### Prerequisites

- Python 3.6 or higher
- `requests` library
- A GitHub account and a personal access token

### Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/yourusername/yourrepositoryname.git
   cd yourrepositoryname
   ```

2. **Install dependencies**:
   Ensure you have Python installed on your system. Then, install the required Python packages using pip:
   ```sh
   pip install requests python-dotenv
   ```

3. **Prepare your `.env` file**:
   Create a `.env` file in the root directory of the project. Add your GitHub personal access token to this file as follows:
   ```
   git_token=YOUR_GITHUB_TOKEN
   ```
   Replace `YOUR_GITHUB_TOKEN` with your actual GitHub token. This token is used to authenticate your requests to GitHub's API.

4. **Organization names file (`organizations.txt`)**:
   Prepare a text file named `organizations.txt` in the root directory with a list of organization names (one per line) that you wish to collect data from. Example:
   ```
   microsoft
   google-research
   apple
   ```

### Running the Application

To run the application and start collecting data, execute the `main.py` script with Python. You can specify the path to your organization names file using the `--orgs` argument:

```sh
python main.py --orgs organizations.txt
```

The script will fetch repository data for the specified organizations and save the information into `repo_summary.csv` and `repo_details.json` files in the root directory.

### Data Dictionary

For detailed information about the data collected and the structure of the output files, refer to the `data_dictionary.md` file in the root directory. This document explains the fields and data types contained in the output files.

### Collected data for Big 5 is available at https://drive.google.com/drive/folders/1CbqZqw7jQGNzE0-4TJMGqW436eT9tejQ?usp=sharing

## Additional Information

- The application respects GitHub's rate limiting by automatically pausing and retrying once the limit resets.
- Ensure your GitHub token has the appropriate permissions to access the data you are requesting.
```