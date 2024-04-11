## Repository Information Data Dictionary

### `repo_info`
Contains detailed information about the repository.
- **`id`**: The unique identifier for the repository (e.g., `647515601`).
- **`node_id`**: The node identifier for the repository (e.g., `"R_kgDOJphN0Q"`).
- **`name`**: The name of the repository (e.g., `"app-store-server-library-java"`).
- **`full_name`**: The full name including the organization (e.g., `"apple/app-store-server-library-java"`).
- **`private`**: Indicates if the repository is private (`false`).
- **`owner`**: Information about the repository owner.
  - **`login`**: The username of the repository owner (e.g., `"apple"`).
  - **`id`**: The unique identifier for the owner (e.g., `10639145`).
  - **`type`**: Type of the owner (e.g., `"Organization"`).
- **`html_url`**: The URL to the repository on GitHub (e.g., `"https://github.com/apple/app-store-server-library-java"`).
- **`description`**: The repository description (e.g., `null` for no description).
- **`fork`**: Indicates if the repository is a fork (`false`).
- **`url`**: API URL of the repository (e.g., `"https://api.github.com/repos/apple/app-store-server-library-java"`).
- **`created_at`**: The creation date of the repository (e.g., `"2023-05-31T00:34:10Z"`).
- **`updated_at`**: The last update date of the repository (e.g., `"2024-03-02T08:58:52Z"`).
- **`pushed_at`**: The last push date of the repository (e.g., `"2024-03-06T16:29:49Z"`).
- **`git_url`**: The Git URL of the repository (e.g., `"git://github.com/apple/app-store-server-library-java.git"`).
- **`stargazers_count`**: Number of stars (e.g., `86`).
- **`watchers_count`**: Number of watchers (e.g., `86`).
- **`language`**: The primary language of the repository (e.g., `"Java"`).
- **`forks_count`**: Number of forks (e.g., `21`).
- **`open_issues_count`**: Number of open issues (e.g., `3`).
- **`license`**: License information of the repository.
  - **`key`**: License key (e.g., `"mit"`).
  - **`name`**: License name (e.g., `"MIT License"`).
- **`forks`**: Number of forks (e.g., `21`).
- **`open_issues`**: Number of open issues (e.g., `3`).
- **`watchers`**: Number of watchers (e.g., `86`).
- **`default_branch`**: The default branch of the repository (e.g., `"main"`).

### `readme`
Contains the README file content in Markdown format. It starts with "# Apple App Store Server Java Library" and includes sections like Installation, Documentation, Usage, and Support.

### `topics`
A list of topics associated with the repository. An empty list indicates no topics.


## Data Dictionary for Repository Summary CSV

The CSV file contains the following columns with the respective data:

- **Organization**: The name of the organization on GitHub that owns the repository (e.g., `apple`).
- **Repo Name**: The name of the repository (e.g., `app-store-server-library-java`).
- **Stars**: The number of stars the repository has received, indicating its popularity (e.g., `86`). Stars are GitHub's way of bookmarking repositories that you find interesting.
- **Forks**: The number of forks, which indicates how many times the repository has been copied by other users (e.g., `21`). Forking a repository allows users to freely experiment with changes without affecting the original project.
- **Primary Language**: The main programming language used in the repository's codebase (e.g., `Java`). This information helps in understanding the technology stack of the project.
- **Topics**: Tags or keywords associated with the repository to improve its discoverability on GitHub. Topics can include technologies used, project purposes, or any other related key phrases. In the provided data, this column is empty, indicating no topics were listed for these repositories.

This dictionary aims to provide clear insights into the dataset, helping users understand the structure and content of the CSV file.
