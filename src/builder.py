from datetime import datetime

def format_recent_repos(repos, limit=5):
    """Formats the most recently updated repositories into markdown list items."""
    markdown_list = ""
    for repo in repos[:limit]:
        name = repo.get("name")
        url = repo.get("html_url")
        desc = repo.get("description") or "No description provided."
        markdown_list += f"- [{name}]({url}) - {desc}\n"
    return markdown_list

def generate_readme(stats, repos, stars):
    """Reads the template, replaces placeholders, and writes to README.md."""
    with open("templates/README_TEMPLATE.md", "r", encoding="utf-8") as file:
        template = file.read()

    # Prepare data
    recent_repos_md = format_recent_repos(repos)
    current_date = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    # Replace placeholders
    new_readme = template.format(
        repo_count=stats.get("public_repos", 0),
        follower_count=stats.get("followers", 0),
        star_count=stars,
        recent_repos=recent_repos_md,
        date=current_date
    )

    # Write the actual README.md to the root directory
    with open("README.md", "w", encoding="utf-8") as file:
        file.write(new_readme)