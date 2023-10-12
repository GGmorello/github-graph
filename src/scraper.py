import json
from datetime import datetime, timedelta
from github import Github
from tqdm import tqdm

# Read access token from .env file
with open('/Users/gabrielemorello/Code/github-graph/src/.env') as f:
    ACCESS_TOKEN = f.read().strip()

# Replace with the repository you want to scrape
REPO_NAME = 'apache/spark'

# Initialize the Github object with the access token
g = Github(ACCESS_TOKEN)

# Get the repository object
repo = g.get_repo(REPO_NAME)

# Load the existing commit data from the file
try:
    with open('commits.json', 'r') as f:
        commit_data = json.load(f)
except FileNotFoundError:
    commit_data = []

# If there is existing commit data, get the last date that was written to file
if commit_data:
    last_commit_date = datetime.fromisoformat(commit_data[-1]['date'])
    # Set the initial date to the day after the last date that was written to file
    date = last_commit_date + timedelta(days=1)
else:
    commits = repo.get_commits().reversed
    first_commit = commits[0]
    first_commit_date = first_commit.commit.author.date
    date = first_commit_date

# Loop through each day from the initial date to the current date
while date < datetime.now():
    # Get the commits for that day
    commits = repo.get_commits(since=date, until=date + timedelta(days=1))

    # print date and number of commits
    print(date.strftime("%Y-%m-%d"), commits.totalCount)

    # If there are commits for that day, append them to the commit data list
    for commit in commits:
        if commit and commit.author and commit.commit and commit.commit.author:
            commit_data.append({
                'repo': REPO_NAME,
                'author': commit.author.login,
                'date': commit.commit.author.date.isoformat()
            })

    # Write the updated commit data to the file
    with open('commits.json', 'w') as f:
        json.dump(commit_data, f, indent=4)

    # Increment the date by one day
    date += timedelta(days=1)
