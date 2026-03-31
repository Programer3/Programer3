import os
import requests

USERNAME = "Programer3"

def get_headers():
    token = os.getenv("GITHUB_TOKEN")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

def fetch_user_stats():
    """Fetches basic user stats like followers and public repos."""
    url = f"https://api.github.com/users/{USERNAME}"
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()

def fetch_user_repos():
    """Fetches the user's repositories to calculate stars and find recent work."""
    url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=updated"
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()

def calculate_total_stars(repos):
    """Iterates through repos to sum up total stars received."""
    return sum(repo.get("stargazers_count", 0) for repo in repos)