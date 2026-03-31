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
    # Use .get() to access the terminal dictionary safely
    t = data.get('terminal', {})
    
    # Mapping exactly to your specific mixed-case keys
    terminal_info = [
        get_terminal_line("OS", t.get('oS', 'N/A')),
        get_terminal_line("Uptime", t.get('uPtime', 'N/A')),
        get_terminal_line("Kernel", t.get('kernel', 'N/A')),
        get_terminal_line("IDE", t.get('iDe', 'N/A')),
        get_terminal_line("Languages.Prog", t.get('languages_prog', 'N/A')),
        get_terminal_line("Languages.Real", t.get('languages_spoken', 'N/A')),
        get_terminal_line("Hobbies", t.get('hObbies', 'N/A')),
        get_terminal_line("Always", t.get('aLways', 'N/A')),
        get_terminal_line("More Info", t.get('mOre info', 'N/A')),
    ]
    
    # Mapping for the Contact section
    contact_info = [
        get_terminal_line("Email", t.get('eMail', 'N/A')),
        get_terminal_line("Discord", t.get('discord', 'N/A')),
    ]

    # Keeping your GitHub Stats logic consistent
    stats_section = (
        f" . Repos:..... {data.get('repos', 0)} {{Contributed: {data.get('contributed', 0)}}} | "
        f"Stars:.......... {data.get('stars', 0)}\n"
        f" . Commits:................ {data.get('commits', 0):,} | "
        f"Followers:....... {data.get('followers', 0)}\n"
        f" . Lines of Code: .... {data.get('loc', 0):,} (Estimated)"
    )

    # Load Template
    with open("templates/README_TEMPLATE.md", "r", encoding="utf-8") as f:
        template = f.read()

    # Injecting all the formatted strings into the template
    final_content = template.format(
        terminal_info="\n".join(terminal_info),
        contact_info="\n".join(contact_info),
        github_stats=stats_section,
        recent_stars=format_starred_repos(data.get('recent_stars', [])),
        last_updated=datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    )

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(final_content)