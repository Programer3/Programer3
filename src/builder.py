import os
from datetime import datetime

def get_terminal_line(key, value, width=20):
    """
    Creates a terminal-style line: 'Key: ........... Value'
    """
    # Calculate how many dots we need to fill the gap
    dots = "." * (width - len(key))
    return f" . {key}:{dots} {value}"

def format_starred_repos(starred_list, limit=5):
    """Formats the recently starred repos into a clean list."""
    if not starred_list:
        return "No recent stars found."
    
    items = []
    for repo in starred_list[:limit]:
        name = repo.get("full_name")
        url = repo.get("html_url")
        desc = repo.get("description") or "No description."
        items.append(f"- [{name}]({url}) - {desc}")
    
    return "\n".join(items)

def generate_readme(data):
    """
    Combines all data into the terminal-style template.
    Expects a dictionary containing 'terminal', 'repos', 'stars', etc.
    """
    # 1. Prepare Terminal Info Section
    t = data['terminal']
    terminal_info = [
        get_terminal_line("OS", t['os']),
        get_terminal_line("Uptime", t['uptime']),
        get_terminal_line("Kernel", t['kernel']),
        get_terminal_line("IDE", t['ide']),
        get_terminal_line("Languages.Prog", t['languages_prog']),
        get_terminal_line("Languages.Real", t['languages_spoken']),
        get_terminal_line("Hobbies", t['hobbies']),
    ]
    
    # 2. Prepare Contact Section
    contact_info = [
        get_terminal_line("Email", t['email']),
        get_terminal_line("Discord", t['discord']),
    ]

    # 3. Prepare GitHub Stats Section
    # Matches the look: 'Repos: .... 47 {Contributed: 90} | Stars: ...... 129'
    stats_section = (
        f" . Repos:..... {data['repos']} {{Contributed: {data['contributed']}}} | "
        f"Stars:.......... {data['stars']}\n"
        f" . Commits:................ {data['commits']:,} | "
        f"Followers:....... {data['followers']}\n"
        f" . Lines of Code: .... {data['loc']:,} (Estimated)"
    )

    # 4. Load Template
    template_path = "templates/README_TEMPLATE.md"
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Could not find {template_path}")

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # 5. Inject Data
    final_content = template.format(
        terminal_info="\n".join(terminal_info),
        contact_info="\n".join(contact_info),
        github_stats=stats_section,
        recent_stars=format_starred_repos(data['recent_stars']),
        last_updated=datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    )

    # 6. Save to root
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(final_content)