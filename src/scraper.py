import argparse
import json
import os
from datetime import datetime, timedelta
from github import Github, GithubException
from tqdm import tqdm


def read_access_token():
    with open('.env') as f:
        return f.read().strip()


def get_repo(repo_name, access_token):
    g = Github(access_token)
    return g.get_repo(repo_name)


def extract_commit_data(commit, repo_name):
    try: 
        if commit and commit.author and commit.author.login and commit.commit and commit.commit.author and commit.commit.author.date:
            return {
                'repo': repo_name,
                'author': commit.author.login,
                'date': commit.commit.author.date.isoformat()
            }
        return None
    except GithubException:
        return None


def load_commit_data():
    try:
        with open('commits.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def get_last_commit_date(commit_data):
    if commit_data:
        return datetime.fromisoformat(commit_data[-1]['date'])
    return None


def get_first_commit_date(repo):
    commits = repo.get_commits().reversed
    first_commit = commits[0]
    return first_commit.commit.author.date


def get_commits_since_date(repo, date):
    return repo.get_commits(since=date, until=date + timedelta(days=1))


def get_all_commits(repo):
    return repo.get_commits()


def scrape_commits(option, repo, commit_data):
    if option == "day":
        last_commit_date = get_last_commit_date(commit_data)
        if last_commit_date:
            date = last_commit_date + timedelta(days=1)
        else:
            date = get_first_commit_date(repo)
        while date < datetime.now():
            commits = get_commits_since_date(repo, date)
            print(date.strftime("%Y-%m-%d"), commits.totalCount)
            for commit in commits:
                commit_dict = extract_commit_data(commit, repo.full_name)
                if commit_dict:
                    commit_data.append(commit_dict)
            date += timedelta(days=1)
    else:
        commits = get_all_commits(repo)
        for commit in tqdm(commits, total=commits.totalCount):
            commit_dict = extract_commit_data(commit, repo.full_name)
            if commit_dict:
                commit_data.append(commit_dict)


def write_commit_data(commit_data, repo_name):
    repo_name = repo_name.replace('/', '_')
    if not os.path.exists('data/' + repo_name):
        os.makedirs('data/' + repo_name)
    with open('data/' + repo_name + '/commits.json', 'w') as f:
        json.dump(commit_data, f, indent=4)


def analyze_users(repo_name):
    repo_name = repo_name.replace('/', '_')
    with open('data/' + repo_name + '/commits.json', 'r') as f:
        commit_data = json.load(f)
    users = {}
    for commit in commit_data:
        if commit['author'] not in users:
            users[commit['author']] = 0
        users[commit['author']] += 1
    with open('data/' + repo_name + '/users.json', 'w') as f:
        json.dump(users, f, indent=4)
    


def main():
    parser = argparse.ArgumentParser(description='Scrape commit data from GitHub repositories.')
    parser.add_argument('repo_names', type=str, nargs='+', help='The names of the repositories in the format "owner/repo".')
    parser.add_argument('--access-token', type=str, help='The GitHub access token to use for authentication.')
    parser.add_argument('--option', type=str, choices=['all', 'day'], default='all', help='The option to use for scraping commits.')
    args = parser.parse_args()

    access_token = args.access_token or read_access_token()
    for repo_name in args.repo_names:
        repo = get_repo(repo_name, access_token)
        commit_data = load_commit_data()
        scrape_commits(args.option, repo, commit_data)
        write_commit_data(commit_data, repo_name)


if __name__ == '__main__':
    main()

