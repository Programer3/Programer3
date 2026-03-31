from github_api import fetch_user_stats, fetch_user_repos, calculate_total_stars
from builder import generate_readme

def main():
    print("Fetching user stats...")
    user_stats = fetch_user_stats()
    
    print("Fetching repository data...")
    repos = fetch_user_repos()
    
    print("Calculating total stars...")
    total_stars = calculate_total_stars(repos)
    
    print("Generating new README.md...")
    generate_readme(user_stats, repos, total_stars)
    
    print("Successfully updated README!")

if __name__ == "__main__":
    main()