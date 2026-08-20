"""
today.py — Auto-generates README.md + terminal.svg for github.com/neelashish
"""

import requests
import os
from datetime import datetime, timezone

# ── Config ─────────────────────────────────────────────────────────────────────
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", "")
USER_NAME    = os.environ.get("USER_NAME", "neelashish")

# Terminal SVG dimensions
SVG_W     = 520      # total width
SVG_PAD   = 18      # left/right padding
TITLE_H   = 26      # title bar height
FONT_SIZE = 11.5    # px
LINE_H    = 17      # px between lines
CHAR_W    = FONT_SIZE * 0.601  # monospace char width ≈ 60% of font-size

# Colors
BG       = "#0d1117"
TITLEBAR = "#161b22"
BORDER   = "#21262d"
GREEN    = "#39d353"
ORANGE   = "#f97316"
BLUE     = "#79c0ff"
YELLOW   = "#e3b341"
WHITE    = "#f0f6fc"
GRAY     = "#8b949e"
DKGRAY   = "#21262d"
CYAN     = "#56d364"
PURPLE   = "#d2a8ff"
RED      = "#ff7b72"


# ── GitHub Stats ───────────────────────────────────────────────────────────────
def get_github_stats():
    headers = {"Authorization": f"token {ACCESS_TOKEN}"} if ACCESS_TOKEN else {}
    stats   = {"repos": "?", "followers": "?", "stars": "?", "uptime": "?"}
    try:
        r    = requests.get(f"https://api.github.com/users/{USER_NAME}", headers=headers, timeout=10)
        user = r.json()
        repos     = user.get("public_repos", 0)
        followers = user.get("followers", 0)
        created   = datetime.strptime(
            user.get("created_at", "2024-01-01T00:00:00Z"), "%Y-%m-%dT%H:%M:%SZ"
        ).replace(tzinfo=timezone.utc)
        delta  = datetime.now(timezone.utc) - created
        years  = delta.days // 365
        months = (delta.days % 365) // 30
        days   = delta.days % 30
        uptime = f"{years} yr, {months} mo, {days} d"
        stars  = 0
        rr = requests.get(
            f"https://api.github.com/users/{USER_NAME}/repos?per_page=100&type=owner",
            headers=headers, timeout=10
        )
        if rr.status_code == 200:
            for repo in rr.json():
                stars += repo.get("stargazers_count", 0)
        stats = {"repos": str(repos), "followers": str(followers),
                 "stars": str(stars), "uptime": uptime}
    except Exception as e:
        print(f"[warn] GitHub API: {e}")
    return stats


# ── SVG helpers ────────────────────────────────────────────────────────────────
def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def svg_line(segments, y):
    """
    segments: list of (text, color) tuples
    Returns a single SVG <text> element with colored <tspan>s.
    """
    x = float(SVG_PAD)
    parts = [f'<text y="{y}" font-family="\'Courier New\',Consolas,monospace" '
             f'font-size="{FONT_SIZE}" xml:space="preserve">']
    for text, color in segments:
        parts.append(f'<tspan x="{x:.1f}" fill="{color}">{esc(text)}</tspan>')
        x += len(text) * CHAR_W
    parts.append("</text>")
    return "".join(parts)


# ── Build info lines ───────────────────────────────────────────────────────────
def info_lines(stats):
    SEP = [("─" * 58, DKGRAY)]
    BLK = [(" ", WHITE)]

    D  = " ............ "  # dot separator
    D2 = " ... "

    rows = [
        [("neelashish", GREEN), ("@github", GRAY)],
        SEP,
        BLK,
        [("  OS    ", YELLOW), (D, GRAY), ("Windows 11", WHITE)],
        [("  Uptime", YELLOW), (D, GRAY), (stats["uptime"], WHITE)],
        [("  Host  ", YELLOW), (D, GRAY), ("github.com/neelashish", BLUE)],
        [("  IDE   ", YELLOW), (D, GRAY), ("VS Code  ·  Jupyter", WHITE)],
        [("  Shell ", YELLOW), (D, GRAY), ("PowerShell", WHITE)],
        BLK,
        [("  Lang", ORANGE), (".Programming", GRAY), (D, GRAY), ("Python, R, SQL, C++", WHITE)],
        [("  Lang", ORANGE), (".ML         ", GRAY), (D, GRAY), ("NumPy, Pandas, Matplotlib", WHITE)],
        [("  Lang", ORANGE), (".Stats      ", GRAY), (D, GRAY), ("Tidyverse, ggplot2, dplyr", WHITE)],
        BLK,
        [("  Learn", PURPLE), (".Now    ", GRAY), (D, GRAY), ("Machine Learning", WHITE)],
        [("  Learn", PURPLE), (".Next   ", GRAY), (D, GRAY), ("Deep Learning", WHITE)],
        [("  Prog ", ORANGE), (".ML     ", GRAY), ("  [", WHITE), ("████", ORANGE),  ("░░░░", DKGRAY), ("] In Progress", WHITE)],
        [("  Prog ", ORANGE), (".LinAlg ", GRAY), ("  [", WHITE), ("██",   BLUE),    ("░░░░░░", DKGRAY), ("] Queued", WHITE)],
        BLK,
        [("  Hobby", CYAN),   (".Anime  ", GRAY), (D, GRAY), ("Naruto  ·  Marvel", WHITE)],
        [("  Hobby", CYAN),   (".Games  ", GRAY), (D, GRAY), ("Strategy / RPG", WHITE)],
        [("  Hobby", CYAN),   (".Read   ", GRAY), (D, GRAY), ("Tech, Sci-Fi", WHITE)],
        BLK,
        SEP,
        BLK,
        [("  LinkedIn ", YELLOW), (D2, GRAY), ("linkedin.com/in/neelashish-b5a50b380", BLUE)],
        [("  X/Twitter", YELLOW), (D2, GRAY), ("@Neelashish_08",                       BLUE)],
        [("  Email    ", YELLOW), (D2, GRAY), ("neelashish0@gmail.com",                 BLUE)],
        BLK,
        SEP,
        BLK,
        [("  Repos:", YELLOW), (f"  {stats['repos']}", GREEN),
         ("    Stars:", YELLOW), (f"  {stats['stars']}", GREEN)],
        [("  Followers:", YELLOW), (f"  {stats['followers']}", GREEN)],
        BLK,
        SEP,
        BLK,
        [('  "Those who break the rules are scum,', GRAY)],
        [('   but those who abandon their friends', GRAY)],
        [('   are worse than scum."', GRAY)],
        [('                       — Hatake Kakashi', ORANGE)],
        BLK,
    ]
    return rows


# ── Generate terminal.svg ──────────────────────────────────────────────────────
def generate_terminal_svg(stats):
    rows = info_lines(stats)
    n    = len(rows)
    H    = TITLE_H + SVG_PAD + n * LINE_H + SVG_PAD

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SVG_W} {H}" '
                 f'width="{SVG_W}" height="{H}">')

    # Background
    parts.append(f'<rect width="{SVG_W}" height="{H}" fill="{BG}" rx="8"/>')

    # Title bar
    parts.append(f'<rect width="{SVG_W}" height="{TITLE_H}" fill="{TITLEBAR}" rx="8"/>')
    parts.append(f'<rect width="{SVG_W}" height="{TITLE_H//2}" y="{TITLE_H//2}" fill="{TITLEBAR}"/>')

    # Border
    parts.append(f'<rect width="{SVG_W-.5}" height="{H-.5}" x=".25" y=".25" '
                 f'fill="none" stroke="{BORDER}" stroke-width=".5" rx="8"/>')

    # Traffic lights
    cy = TITLE_H // 2
    parts.append(f'<circle cx="16" cy="{cy}" r="4" fill="#ff5f57"/>')
    parts.append(f'<circle cx="30" cy="{cy}" r="4" fill="#ffbd2e"/>')
    parts.append(f'<circle cx="44" cy="{cy}" r="4" fill="#28c941"/>')

    # Window title
    parts.append(f'<text x="{SVG_W//2}" y="{cy}" text-anchor="middle" '
                 f'fill="{GRAY}" font-family="\'Courier New\',monospace" '
                 f'font-size="10" dominant-baseline="middle">'
                 f'neelashish@github — bash</text>')

    # Content lines
    for i, segs in enumerate(rows):
        baseline = TITLE_H + SVG_PAD + i * LINE_H + FONT_SIZE
        parts.append(svg_line(segs, baseline))

    parts.append("</svg>")
    return "\n".join(parts)


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    print("Fetching GitHub stats...")
    stats = get_github_stats()

    print("Generating terminal SVG...")
    svg = generate_terminal_svg(stats)
    with open("terminal.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("  -> terminal.svg written")

    print("Writing README.md...")
    readme = """\
<div align="center">

<table border="0" cellspacing="0" cellpadding="10">
<tr>
<td valign="top" align="center">
<img src="kakashi.jpg" width="370" alt="Kakashi ASCII Art"/>
</td>
<td valign="top" align="center">
<img src="terminal.svg" width="470" alt="System Info"/>
</td>
</tr>
</table>

<br/>

<img src="heartbeat.svg" width="780" alt="Chakra Monitor"/>

<br/>

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/neelashish-b5a50b380/)
[![X](https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/Neelashish_08)
[![Email](https://img.shields.io/badge/Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:neelashish0@gmail.com)

<br/>

<img src="https://github.com/neelashish/neelashish/blob/output/github-snake-dark.svg" alt="Snake animation"/>

</div>
"""
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)
    print("  -> README.md written")
    print("[OK] All done!")


if __name__ == "__main__":
    main()
