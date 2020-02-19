# You should write a function that will take as input a GitHub user ID.
# The output from the function will be a list of the names of the repositories that the user has,
# along with the number of commits that are in each of the listed repositories.

import json

import requests

github_repos_api = "https://api.github.com/users/{0}/repos"
github_repos_commits_api = "https://api.github.com/repos/{0}/{1}/commits"


def user_github_activity():
    """
    Gets users github repos based on user id
    """
    github_activity = list()
    user_name = prompt_user()

    repos = get_user_repos(user_name)
    if repos is not None:
        repo: dict
        for repo in repos:
            repo_name = repo.get('name')
            if isinstance(repo_name, str):
                num_commits = get_user_commits_for_repos(user_name, repo_name)
                github_activity.append({
                    'repo': repo_name,
                    'commits': num_commits
                })

    if len(github_activity) > 0:
        for activity in github_activity:
            pretty_print_repo_info(activity.get('repo'), activity.get('commits'))
    else:
        print('There are no repositories for user: {0}'.format(user_name))


def get_user_repos(user: str) -> list:
    # Gets repos for a given user
    response = requests.get(github_repos_api.format(user))

    if response.status_code == 200:
        return json.loads(response.content)
    else:
        return []


def get_user_commits_for_repos(user: str, repo: str) -> int:
    # Gets number of commits for a given user's repo
    response = requests.get(github_repos_commits_api.format(user, repo))

    if response.status_code == 200:
        return len(json.loads(response.content))
    else:
        return 0


def pretty_print_repo_info(repo: int, commits: int) -> None:
    return print("Repo: {0} Number of commits: {1}".format(repo, commits))


def prompt_user() -> str:
    return input("What's your github username? ")


if __name__ == '__main__':
    user_github_activity()
