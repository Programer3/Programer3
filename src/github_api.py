import os
import requests
from datetime import datetime

USERNAME = "Programer3"

# ==========================================
# 1. STATIC TERMINAL CONFIGURATION
# Modify these to match your personal setup
# ==========================================
TERMINAL_CONFIG = {
    "oS": "Windows 11 Pro, Kali Linux (WSL)",
    # "uPtime": "Always learning",
    "kernel": "👀",
    "iDe": "VSCode, Astudio, JetBrains",
    "prog_languages": "Python, Java, C++, Dart",
    "languages_spoken": "Hindi, English",
    "hObbies": "Lerning, Open Source, Gaming",
    "eMail": "amankmcs@gmail.com",
    "aLways": "Curious about new tech and open source projects",
    "mOre info": "👈 On the left side of screen",
    "Fav Casing": "Obviously Pascal then camelCase, look 👆"
}

# ==========================================
# 2. GITHUB API HELPERS
# ==========================================
def get_headers():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable is not set!")
    return {"Authorization": f"Bearer {token}"}

def run_graphql_query(query):
    """Executes a GraphQL query against GitHub's API."""
    url = "https://api.github.com/graphql"
    response = requests.post(url, json={'query': query}, headers=get_headers())
    response.raise_for_status()
    return response.json()

# ==========================================
# 3. DATA FETCHING FUNCTIONS
# ==========================================

def fetch_basic_user_stats():
    """Fetches followers, following, and basic profile info."""
    url = f"https://api.github.com/users/{USERNAME}"
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()

def fetch_recent_stars(limit=5):
    """Fetches the repositories the user has recently starred."""
    url = f"https://api.github.com/users/{USERNAME}/starred?per_page={limit}&sort=created&direction=desc"
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()

def fetch_advanced_stats():
    """
    Uses GraphQL to fetch complex stats in a single network request:
    Total Commits (this year), Total Contributed Repos, and Total Stars Earned.
    """
    query = f"""
    query {{
      user(login: "{USERNAME}") {{
        repositoriesContributedTo(first: 1, contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, REPOSITORY]) {{
          totalCount
        }}
        contributionsCollection {{
          totalCommitContributions
          restrictedContributionsCount
        }}
        repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {{
          totalCount
          nodes {{
            stargazerCount
          }}
        }}
      }}
    }}
    """
    data = run_graphql_query(query)
    user_data = data['data']['user']
    
    # Calculate Total Stars Earned
    repos = user_data['repositories']['nodes']
    total_stars_earned = sum(repo['stargazerCount'] for repo in repos)
    
    # Calculate Total Commits (Public + Private this year)
    collections = user_data['contributionsCollection']
    total_commits = collections['totalCommitContributions'] + collections['restrictedContributionsCount']
    
    return {
        "contributed_repos": user_data['repositoriesContributedTo']['totalCount'],
        "total_commits_this_year": total_commits,
        "total_stars_earned": total_stars_earned,
        "owned_repos": user_data['repositories']['totalCount']
    }

def fetch_comprehensive_stats():
    # 1. Basic User Data (Following, Created At)
    user_url = f"https://api.github.com/users/{USERNAME}"
    user_data = requests.get(user_url, headers=get_headers()).json()
    
    # 2. Repo Data (Size, Max Commits)
    repo_url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100"
    repos = requests.get(repo_url, headers=get_headers()).json()
    
    total_kb = sum(repo.get('size', 0) for repo in repos)
    # Convert KB to MB/GB for readability
    size_str = f"{total_kb / 1024:.2f} MB" if total_kb < 1048576 else f"{total_kb / 1048576:.2f} GB"
    
    # 3. Years on GitHub (Since 2020)
    current_year = datetime.utcnow().year
    years_active = current_year - 2020

    # 4. Coding Hours (ESTIMATION: 0.75 hours per commit as a benchmark)
    # Note: For real hours, you'd need a WakaTime API key.
    estimated_hours = int(data.get('commits', 0)) * 0.75

    return {
        "years_active": years_active,
        "following": user_data.get('following', 0),
        "total_size": size_str,
        "coding_hours": f"{estimated_hours:,}",
        # These usually require paginating through all events or using a 3rd party
        # We'll set these as placeholders for now
        "current_streak": "12 Days", 
        "best_streak": "45 Days"
    }

def fetch_lines_of_code():
    """
    Approximates Lines of Code (LOC) by fetching language bytes across all owned repos.
    Note: GitHub does not expose exact global addition/deletion LOC easily via API.
    Most metrics tools use the repository languages endpoint to estimate this.
    """
    url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&type=owner"
    repos = requests.get(url, headers=get_headers()).json()
    
    total_bytes = 0
    for repo in repos:
        # Skip forks to only count your original code
        if repo['fork']:
            continue
            
        lang_url = repo['languages_url']
        lang_data = requests.get(lang_url, headers=get_headers()).json()
        
        # Sum the bytes of code for each language in the repo
        total_bytes += sum(lang_data.values())
    
    # Extremely rough estimation: average 30 bytes per line of code
    estimated_loc = total_bytes // 30 
    
    return {
        "total_bytes": total_bytes,
        "estimated_lines": estimated_loc
    }

def get_all_data():
    """Master function to gather everything into one clean dictionary."""
    basic = fetch_basic_user_stats()
    advanced = fetch_advanced_stats()
    loc = fetch_lines_of_code()
    recent_stars = fetch_recent_stars()
    
    return {
        "terminal": TERMINAL_CONFIG,
        "followers": basic.get("followers", 0),
        "repos": advanced["owned_repos"],
        "contributed": advanced["contributed_repos"],
        "stars": advanced["total_stars_earned"],
        "commits": advanced["total_commits_this_year"],
        "loc": loc["estimated_lines"],
        "recent_stars": recent_stars
    }