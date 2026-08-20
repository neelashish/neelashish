"""
today.py — Auto-generates README.md for github.com/neelashish
Layout: Kakashi ASCII art (left) + live neofetch info panel (right)
"""

import requests
import os
import math
from datetime import datetime, timezone

# ── Config ────────────────────────────────────────────────────────────────────
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", "")
USER_NAME    = os.environ.get("USER_NAME", "neelashish")
ASCII_PATH   = "kakashi_ascii.txt.txt"

ASCII_WIDTH  = 42   # target chars wide for the ASCII panel
ASCII_HEIGHT = 40   # target lines tall  (must match INFO_LINES count)

# ── GitHub Stats ──────────────────────────────────────────────────────────────
def get_github_stats():
    headers = {"Authorization": f"token {ACCESS_TOKEN}"} if ACCESS_TOKEN else {}
    stats   = {"repos": "?", "followers": "?", "stars": "?", "uptime": "?"}

    try:
        r    = requests.get(f"https://api.github.com/users/{USER_NAME}", headers=headers, timeout=10)
        user = r.json()

        repos     = user.get("public_repos", 0)
        followers = user.get("followers", 0)

        # Account age
        created = datetime.strptime(
            user.get("created_at", "2024-01-01T00:00:00Z"), "%Y-%m-%dT%H:%M:%SZ"
        ).replace(tzinfo=timezone.utc)
        delta  = datetime.now(timezone.utc) - created
        years  = delta.days // 365
        months = (delta.days % 365) // 30
        days   = delta.days % 30
        uptime = f"{years} yr, {months} mo, {days} d"

        # Star count across all repos
        stars = 0
        rep_r = requests.get(
            f"https://api.github.com/users/{USER_NAME}/repos?per_page=100&type=owner",
            headers=headers, timeout=10
        )
        if rep_r.status_code == 200:
            for repo in rep_r.json():
                stars += repo.get("stargazers_count", 0)

        stats = {
            "repos":     str(repos),
            "followers": str(followers),
            "stars":     str(stars),
            "uptime":    uptime,
        }
    except Exception as e:
        print(f"[warn] GitHub API error: {e}")

    return stats


# ── ASCII Loader ──────────────────────────────────────────────────────────────
def load_ascii(path, target_w=ASCII_WIDTH, target_h=ASCII_HEIGHT):
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = [l.rstrip("\r\n") for l in f.readlines()]
    except FileNotFoundError:
        return [" " * target_w] * target_h

    # Trim blank border lines
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()

    if not lines:
        return [" " * target_w] * target_h

    orig_h = len(lines)
    orig_w = max(len(l) for l in lines) or 1

    result = []
    for i in range(target_h):
        li   = min(int(i * orig_h / target_h), orig_h - 1)
        line = lines[li].ljust(orig_w)
        row  = ""
        for j in range(target_w):
            ci   = int(j * orig_w / target_w)
            row += line[ci] if ci < len(line) else " "
        result.append(row)

    return result


# ── Info Panel ────────────────────────────────────────────────────────────────
def build_info(stats):
    D  = " ............... "
    HL = "─" * 55

    lines = [
        f"neelashish@github",
        HL,
        "",
        f"  OS       {D}Windows 11",
        f"  Uptime   {D}{stats['uptime']}",
        f"  Host     {D}github.com/neelashish",
        f"  IDE      {D}VS Code  ·  Jupyter",
        f"  Shell    {D}PowerShell",
        "",
        f"  Languages.Programming ... Python, R, SQL, C++",
        f"  Languages.ML ............ NumPy, Pandas, Matplotlib",
        f"  Languages.Stats ......... Tidyverse, ggplot2, dplyr",
        "",
        f"  Learning.Now ............ Machine Learning",
        f"  Learning.Next ........... Deep Learning",
        f"  Progress.ML   [ ████░░░░ ]  In Progress",
        f"  Progress.LA   [ ██░░░░░░ ]  In Progress",
        "",
        f"  Hobbies.Anime ........... Naruto  ·  Marvel",
        f"  Hobbies.Games ........... Strategy / RPG",
        f"  Hobbies.Read ............ Tech, Sci-Fi",
        "",
        HL,
        "",
        f"  LinkedIn  ... linkedin.com/in/neelashish-b5a50b380",
        f"  X/Twitter ... @Neelashish_08",
        f"  Email  ...... neelashish0@gmail.com",
        "",
        HL,
        "",
        f"  Repos: {stats['repos']:>4}     |  Stars:     {stats['stars']:>4}",
        f"  Followers: {stats['followers']:>4}",
        "",
        HL,
        "",
        f'  "Those who break the rules are scum,',
        f'   but those who abandon their friends',
        f'   are worse than scum."',
        f"                       — Hatake Kakashi",
        "",
        "",
    ]

    return lines


# ── Combine ───────────────────────────────────────────────────────────────────
def combine(ascii_lines, info_lines):
    n = max(len(ascii_lines), len(info_lines))
    rows = []
    for i in range(n):
        left  = ascii_lines[i] if i < len(ascii_lines) else ""
        right = info_lines[i]  if i < len(info_lines)  else ""
        rows.append(f"{left.ljust(ASCII_WIDTH)}   {right}")
    return "\n".join(rows)


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("Fetching GitHub stats...")
    stats = get_github_stats()

    print("Loading ASCII art...")
    ascii_lines = load_ascii(ASCII_PATH, ASCII_WIDTH, ASCII_HEIGHT)

    print("Building info panel...")
    info_lines  = build_info(stats)

    # Pad the shorter panel so they align
    diff = len(info_lines) - len(ascii_lines)
    if diff > 0:
        ascii_lines += [" " * ASCII_WIDTH] * diff
    elif diff < 0:
        info_lines  += [""] * (-diff)

    print("Combining panels...")
    terminal = combine(ascii_lines, info_lines)

    readme = f"```\n{terminal}\n```\n"

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)

    print("[OK] README.md written successfully!")


if __name__ == "__main__":
    main()
