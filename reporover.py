# combined_script.py

from bs4 import BeautifulSoup
from github import BadCredentialsException, Github
import requests
import sqlite3
import configparser
import time
import os
from github import GithubException
from tqdm import tqdm


# Global variable for repo_url
repo_url = ""

def parse_repo_url(repo_url):
    # Extract the username and repository name from the GitHub URL
    username_repo = repo_url.split('/')[-2:]
    return username_repo[0], username_repo[1]

def last_commit_date(repo_url):
    # Retrieve the last commit timestamp from the GitHub repository using GitHub API
    username, repo_name = parse_repo_url(repo_url)
    g = Github()
    repo = g.get_repo(f"{username}/{repo_name}")
    commits = repo.get_commits()

    if commits.totalCount > 0:
        last_commit = commits[0]
        return last_commit.commit.author.date.isoformat()
    else:
        return None

def commit_history(repo_url):
    # Retrieve commit history from the GitHub repository
    username, repo_name = parse_repo_url(repo_url)
    g = Github()
    repo = g.get_repo(f"{username}/{repo_name}")
    commits = repo.get_commits()
    commit_data = []

    for commit in commits:
        commit_data.append({
            "sha": commit.sha,
            "message": commit.commit.message,
            "author": commit.author.login,
            "date": commit.commit.author.date.isoformat()
        })

    return commit_data

def console_updates(message):
    # Display real-time updates in the console
    print(message)

def individual_log_files(repo_url, log_folder_path, commit_data):
    # Create individual log files for each repository in a subfolder
    repo_name = parse_repo_url(repo_url)[1]
    log_file_path = os.path.join(log_folder_path, f"{repo_name}_log.txt")

    with open(log_file_path, 'a') as log_file:
        log_file.write(f"Repository: {repo_url}\n")
        log_file.write("Individual Log Content\n")
        log_file.write(f"Last Commit Timestamp: {commit_data[0]['date']}\n")
        log_file.write("Commit History:\n")
        for commit in commit_data:
            log_file.write(f"Sha: {commit['sha']}\n")
            log_file.write(f"Message: {commit['message']}\n")
            log_file.write(f"Author: {commit['author']}\n")
            log_file.write(f"Date: {commit['date']}\n")
            log_file.write("\n")

    print(f"Individual log file created at: {log_file_path}")

def unified_log_option(log_folder_path, combined_log_file):
    # Append log data to a combined log file in a subfolder for consolidated information
    repo_name = parse_repo_url(repo_url)[1]
    log_file_path = os.path.join(log_folder_path, f"{repo_name}_log.txt")
    combined_log_path = os.path.join(log_folder_path, combined_log_file)

    with open(log_file_path, 'r') as individual_log, open(combined_log_path, 'a') as combined_log:
        combined_log.write(f"Repository: {repo_url}\n")
        combined_log.write("Combined Log Content\n")
    print(f"Combined log file updated at: {combined_log_path}")

def html_logs(repo_url, log_folder_path):
    # Generate HTML logs for enhanced readability in a subfolder
    repo_name = parse_repo_url(repo_url)[1]
    html_log_path = os.path.join(log_folder_path, f"{repo_name}_log.html")

    with open(html_log_path, 'w') as html_log:
        html_log.write(f"<html><body><h1>Repository: {repo_url}</h1>")
        html_log.write("<p>HTML Log Content</p></body></html>")
    print(f"HTML log file created at: {html_log_path}")

def ini_file_setup(file_path='config.ini'):
    # Set up a user-friendly config.ini file for customization
    config = configparser.ConfigParser()

    # Read the configuration file
    config.read(file_path)

    # Check if the github_token contains a placeholder
    github_token = config.get('GitHub', 'github_token', fallback=None)
    if github_token and '${' in github_token and '}' in github_token:
        # The token contains a placeholder, try to replace it with an environment variable
        env_variable_name = github_token.strip('${}').upper()
        github_token = os.getenv(env_variable_name, fallback=None)

    return config, github_token

def get_github_instance(config):
    # Get GitHub instance with or without a token based on the configuration
    github_token = config.get('GitHub', 'github_token', fallback=None)
    if github_token:
        return Github(github_token)
    else:
        return Github()

def handle_api_error(error):
    # Handle GitHub API errors, including rate limit exceeded
    if hasattr(error, 'status') and error.status == 403:
        # Rate limit exceeded, back off and retry
        backoff_time = int(error.headers.get('Retry-After', 60))
        print(f"Rate limit exceeded. Retrying after {backoff_time} seconds.")
        for remaining_seconds in range(backoff_time, 0, -1):
            print(f"Next attempt in {remaining_seconds} seconds...", end='\r')
            time.sleep(1)
        print()  # Move to the next line after the countdown

    else:
        # Handle other API errors
        print(f"GitHub API error: {error}")
        # Add appropriate handling for other types of errors

def automation(repo_url, auto_run_interval, log_folder_path, github_instance):
    config, github_token = ini_file_setup('config.ini')  # Specify the path to the INI file
    last_commit_timestamp_path = os.path.join(log_folder_path, 'last_commit_timestamp.txt')

    # Read the last commit timestamp from the file
    if os.path.exists(last_commit_timestamp_path):
        with open(last_commit_timestamp_path, 'r') as timestamp_file:
            last_commit_timestamp = timestamp_file.read().strip()
    else:
        last_commit_timestamp = None

    while True:
        print(f"Running script for {repo_url}...")

        # Calculate the time until the next update
        time_until_next_update = auto_run_interval * 60  # Convert minutes to seconds

        # Display the countdown in the console
        while time_until_next_update > 0:
            minutes, seconds = divmod(time_until_next_update, 60)
            countdown_str = f"Time until next update: {minutes} minutes and {seconds} seconds"
            print(countdown_str, end='\r')  # Print on the same line
            time.sleep(1)
            time_until_next_update -= 1

        print()  # Move to the next line after the countdown

        try:
            # Retrieve the GitHub repository dynamically
            repo = github_instance.get_repo(f"{repo_url.split('/')[-2]}/{repo_url.split('/')[-1]}")

            last_commit_timestamp_repo = last_commit_date(repo_url)

            if last_commit_timestamp_repo and last_commit_timestamp_repo != last_commit_timestamp:
                # Only process if there are new commits since the last update
                commit_data = commit_history(repo_url)

                # Update the last commit timestamp file
                with open(last_commit_timestamp_path, 'w') as timestamp_file:
                    timestamp_file.write(last_commit_timestamp_repo)

                individual_log_files(repo_url, log_folder_path, commit_data)
                unified_log_option(log_folder_path, config['LogPreferences']['combined_log_file'])
                html_logs(repo_url, log_folder_path)

                customization(config)  # Pass the config to the customization function

                initialize_database()

                repo_data = {
                    'repo_url': repo_url,
                    'last_commit_date': last_commit_timestamp_repo,
                    'stars': repo.stargazers_count,
                    'forks': repo.forks_count,
                    'latest_release': 'v1.0',
                    'description': repo.description,  # Use the actual repository description
                    'commit_history': commit_data
                }

                insert_repository_data(repo_data)

        except GithubException as e:
            print(f"Error retrieving repository data: {e}")

        time.sleep(auto_run_interval * 60)  # Convert minutes to seconds


def customization(config):
    # Add customization logic based on the provided config
    log_stars_forks = config.getboolean('LogPreferences', 'log_stars_forks')
    compare_popularity = config.getboolean('LogPreferences', 'compare_popularity')
    log_latest_release = config.getboolean('LogPreferences', 'log_latest_release')

    if log_stars_forks:
        console_updates("[Not Functional] - Logging stars and forks information.")
        # Additional logic for logging stars and forks coming soon

    if compare_popularity:
        console_updates("[Not Functional] - Comparing repository popularity.")
        # Additional logic for comparing repository popularity coming soon

    if log_latest_release:
        console_updates("[Not Functional] - Logging information about the latest release.")
        # Additional logic for logging latest release information coming soon

def initialize_database():
    # Initialize an SQLite database for efficient data storage
    conn = sqlite3.connect('repository_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS repositories
                      (repo_url TEXT, last_commit_date TEXT, stars INTEGER, forks INTEGER,
                       latest_release TEXT, description TEXT, commit_history TEXT)''')
    conn.commit()
    conn.close()

def insert_repository_data(repo_data):
    # Insert repository data into the database for historical tracking
    conn = sqlite3.connect('repository_data.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO repositories VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (repo_data['repo_url'], repo_data['last_commit_date'], repo_data['stars'],
                    repo_data['forks'], repo_data['latest_release'], repo_data['description'],
                    str(repo_data['commit_history'])))
    conn.commit()
    conn.close()

def get_all_repository_data():
    # Retrieve all repository data from the database
    conn = sqlite3.connect('repository_data.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM repositories''')
    repositories = cursor.fetchall()
    conn.close()
    return repositories

if __name__ == "__main__":
    # Read the repository URLs and GitHub token from the config.ini file
    config, github_token = ini_file_setup()

    # Display loaded settings
    print("Loaded settings from config.ini:")
    for section in config.sections():
        print(f"  [{section}]")
        for key, value in config.items(section):
            # Redact the actual GitHub token if present
            if key.lower() == 'github_token':
                value = '*' * len(value)
            print(f"    {key}: {value}")

    # If github_token is still None or empty, prompt the user to enter it
    if not github_token or not github_token.strip():
        while True:
            github_token = input("Enter your GitHub token: ")
            try:
                # Check if the entered GitHub token is valid
                g = Github(github_token)
                g.get_user()
                print("GitHub token is valid.")
                break
            except BadCredentialsException:
                print("Invalid GitHub token. Please try again.")

    # Display whether a GitHub token is set
    if github_token:
        print("\nGitHub token is set.")
    else:
        print("\nNo GitHub token is set. Please provide a token when prompted.")

    # Use the token to get the GitHub instance
    g = Github(github_token)

    # Read the repository URLs from the config.ini file
    repo_links = [url.strip() for url in config['GitHubRepos']['links'].split('\n') if url.strip()]


    # Run automation for each repository
    for repo_url in repo_links:
        # Skip empty lines
        if not repo_url.strip():
            continue

        # Create a subfolder for each repository
        repo_name = parse_repo_url(repo_url)[1]
        log_folder_path = os.path.join(os.getcwd(), repo_name)

        if not os.path.exists(log_folder_path):
            os.makedirs(log_folder_path)

        automation(repo_url.strip(), config.getint('Scheduling', 'auto_run_interval'), log_folder_path, g)
