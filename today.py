"""
today.py — Auto-generates README.md + SVG assets for github.com/neelashish
SVGs generated: terminal.svg, heartbeat.svg, quote.svg
"""

import requests
import os
import math
from datetime import datetime, timezone

# ── Config ─────────────────────────────────────────────────────────────────────
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", "")
USER_NAME    = os.environ.get("USER_NAME", "neelashish")

# Terminal SVG
SVG_W     = 510
SVG_PAD   = 18
TITLE_H   = 26
FONT_SIZE = 11.5
LINE_H    = 17
CHAR_W    = FONT_SIZE * 0.601

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
    return (t.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))

def svg_line(segments, y):
    x = float(SVG_PAD)
    parts = [f'<text y="{y}" font-family="\'Courier New\',Consolas,monospace" '
             f'font-size="{FONT_SIZE}" xml:space="preserve">']
    for text, color in segments:
        parts.append(f'<tspan x="{x:.1f}" fill="{color}">{esc(text)}</tspan>')
        x += len(text) * CHAR_W
    parts.append("</text>")
    return "".join(parts)


# ── Terminal info lines ────────────────────────────────────────────────────────
def info_lines(stats):
    SEP = [("─" * 55, DKGRAY)]
    BLK = [(" ", WHITE)]
    D   = " ............ "

    rows = [
        [("neelashish", GREEN), ("@github", GRAY)],
        SEP,
        BLK,
        [("  OS    ", YELLOW), (D, GRAY), ("Windows 11",              WHITE)],
        [("  Uptime", YELLOW), (D, GRAY), (stats["uptime"],           WHITE)],
        [("  Host  ", YELLOW), (D, GRAY), ("github.com/neelashish",   BLUE )],
        [("  IDE   ", YELLOW), (D, GRAY), ("VS Code  ·  Jupyter",     WHITE)],
        [("  Shell ", YELLOW), (D, GRAY), ("PowerShell",              WHITE)],
        BLK,
        [("  Lang", ORANGE), (".Programming", GRAY), (D, GRAY), ("Python, R, SQL, C++",       WHITE)],
        [("  Lang", ORANGE), (".ML         ", GRAY), (D, GRAY), ("NumPy, Pandas, Matplotlib", WHITE)],
        [("  Lang", ORANGE), (".Stats      ", GRAY), (D, GRAY), ("Tidyverse, ggplot2, dplyr", WHITE)],
        BLK,
        [("  Learn", PURPLE), (".Now  ", GRAY), (D, GRAY), ("Machine Learning", WHITE)],
        [("  Learn", PURPLE), (".Next ", GRAY), (D, GRAY), ("Deep Learning",    WHITE)],
        [("  Prog ", ORANGE), (".ML   ", GRAY), ("  [", WHITE),
         ("\u2588\u2588\u2588\u2588", ORANGE), ("\u2591\u2591\u2591\u2591", DKGRAY), ("] In Progress", WHITE)],
        [("  Prog ", ORANGE), (".Math ", GRAY), ("  [", WHITE),
         ("\u2588\u2588",     BLUE),   ("\u2591\u2591\u2591\u2591\u2591\u2591", DKGRAY), ("] In Progress", WHITE)],
        BLK,
        SEP,
        BLK,
        [("  Repos:", YELLOW),     (f"  {stats['repos']:<5}",     GREEN),
         ("  Stars:",    YELLOW),  (f"  {stats['stars']:<5}",     GREEN)],
        [("  Followers:", YELLOW), (f"  {stats['followers']}", GREEN)],
        BLK,
        SEP,
        BLK,
        [('  "Those who break the rules are scum,',      GRAY  )],
        [('   but those who abandon their friends',       GRAY  )],
        [('   are worse than scum."',                     GRAY  )],
        [('                       \u2014 Hatake Kakashi', ORANGE)],
        BLK,
    ]
    return rows


# ── Generate terminal.svg ──────────────────────────────────────────────────────
def generate_terminal_svg(stats):
    rows = info_lines(stats)
    H    = TITLE_H + SVG_PAD + len(rows) * LINE_H + SVG_PAD

    p = []
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SVG_W} {H}" '
             f'width="{SVG_W}" height="{H}">')
    p.append(f'<rect width="{SVG_W}" height="{H}" fill="{BG}" rx="8"/>')
    p.append(f'<rect width="{SVG_W}" height="{TITLE_H}" fill="{TITLEBAR}" rx="8"/>')
    p.append(f'<rect width="{SVG_W}" height="{TITLE_H//2}" y="{TITLE_H//2}" fill="{TITLEBAR}"/>')
    p.append(f'<rect width="{SVG_W-.5}" height="{H-.5}" x=".25" y=".25" '
             f'fill="none" stroke="{BORDER}" stroke-width=".5" rx="8"/>')
    cy = TITLE_H // 2
    p.append(f'<circle cx="16" cy="{cy}" r="4" fill="#ff5f57"/>')
    p.append(f'<circle cx="30" cy="{cy}" r="4" fill="#ffbd2e"/>')
    p.append(f'<circle cx="44" cy="{cy}" r="4" fill="#28c941"/>')
    p.append(f'<text x="{SVG_W//2}" y="{cy}" text-anchor="middle" fill="{GRAY}" '
             f'font-family="\'Courier New\',monospace" font-size="10" dominant-baseline="middle">'
             f'neelashish@github \u2014 bash</text>')

    for i, segs in enumerate(rows):
        baseline = TITLE_H + SVG_PAD + i * LINE_H + FONT_SIZE
        p.append(svg_line(segs, baseline))

    p.append("</svg>")
    return "\n".join(p)


# ── Generate quote.svg ─────────────────────────────────────────────────────────
def generate_quote_svg():
    W, H = 320, 210
    p = []
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')

    # Background
    p.append(f'<rect width="{W}" height="{H}" fill="{BG}" rx="10"/>')

    # Title bar
    p.append(f'<rect width="{W}" height="26" fill="{TITLEBAR}" rx="10"/>')
    p.append(f'<rect width="{W}" height="13" y="13" fill="{TITLEBAR}"/>')

    # Border
    p.append(f'<rect width="{W-.5}" height="{H-.5}" x=".25" y=".25" '
             f'fill="none" stroke="{BORDER}" stroke-width=".5" rx="10"/>')

    # Traffic lights
    p.append(f'<circle cx="16" cy="13" r="4" fill="#ff5f57"/>')
    p.append(f'<circle cx="30" cy="13" r="4" fill="#ffbd2e"/>')
    p.append(f'<circle cx="44" cy="13" r="4" fill="#28c941"/>')

    # Window title
    p.append(f'<text x="{W//2}" y="13" text-anchor="middle" fill="{GRAY}" '
             f'font-family="\'Courier New\',monospace" font-size="10" dominant-baseline="middle">'
             f'kakashi.hatake</text>')

    # Orange accent top bar
    p.append(f'<rect x="14" y="34" width="4" height="142" fill="{ORANGE}" rx="2"/>')

    # Big quote marks
    p.append(f'<text x="26" y="62" fill="{ORANGE}" font-family="Georgia,serif" '
             f'font-size="48" opacity="0.25">\u201c</text>')

    # Quote lines
    font = f'font-family="\'Courier New\',Consolas,monospace" font-size="11"'
    lines = [
        ("Those who break the",   GRAY),
        ("rules are scum,",        GRAY),
        ("",                       GRAY),
        ("but those who abandon",  GRAY),
        ("their friends are",      GRAY),
        ("worse than scum.",       GRAY),
        ("",                       GRAY),
        ("\u2014 Hatake Kakashi",  ORANGE),
    ]
    for i, (txt, col) in enumerate(lines):
        y = 58 + i * 17
        p.append(f'<text x="26" y="{y}" fill="{col}" {font}>{esc(txt)}</text>')

    # Bottom Sharingan dots (decorative)
    for i, col in enumerate([ORANGE, "#c00", ORANGE]):
        p.append(f'<circle cx="{W//2 - 16 + i*16}" cy="{H-14}" r="3" fill="{col}" opacity="0.6"/>')

    p.append("</svg>")
    return "\n".join(p)


# ── Generate heartbeat.svg (organic mathematical wave) ─────────────────────────
def generate_heartbeat_svg():
    W, H      = 800, 110
    TITLE_H2  = 26
    BASE_Y    = 67   # baseline y
    CLIP_TOP  = TITLE_H2
    CLIP_BOT  = H - 14  # above status bar

    def wave_y(x):
        """Superposition of sine waves — all periods divide evenly into 800 for seamless loop."""
        y = BASE_Y
        y -= 10 * math.sin(x * 2 * math.pi / 800)
        y -=  6 * math.sin(x * 2 * math.pi / 200 + 0.7)
        y -=  3 * math.sin(x * 2 * math.pi /  80 + 1.4)
        y -= 1.5 * math.sin(x * 2 * math.pi /  40 + 0.3)
        return max(CLIP_TOP + 8, min(CLIP_BOT - 6, y))

    # Build 1600px path (two seamless loops), sample every 3px
    pts = [f"{x},{wave_y(x):.2f}" for x in range(0, 1601, 3)]
    wave_path = "M " + " L ".join(pts)

    p = []
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')

    p.append(f'''  <defs>
    <clipPath id="ekgClip">
      <rect x="0" y="{CLIP_TOP}" width="{W}" height="{CLIP_BOT - CLIP_TOP}"/>
    </clipPath>
    <filter id="glow" x="-20%" y="-40%" width="140%" height="180%">
      <feGaussianBlur stdDeviation="2.5" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>''')

    # Background
    p.append(f'  <rect width="{W}" height="{H}" fill="{BG}" rx="8"/>')

    # Title bar
    p.append(f'  <rect width="{W}" height="{TITLE_H2}" fill="{TITLEBAR}" rx="8"/>')
    p.append(f'  <rect width="{W}" height="{TITLE_H2//2}" y="{TITLE_H2//2}" fill="{TITLEBAR}"/>')

    # Border
    p.append(f'  <rect width="{W-.5}" height="{H-.5}" x=".25" y=".25" '
             f'fill="none" stroke="{BORDER}" stroke-width=".5" rx="8"/>')

    # Traffic lights
    cy2 = TITLE_H2 // 2
    p.append(f'  <circle cx="16" cy="{cy2}" r="4" fill="#ff5f57"/>')
    p.append(f'  <circle cx="30" cy="{cy2}" r="4" fill="#ffbd2e"/>')
    p.append(f'  <circle cx="44" cy="{cy2}" r="4" fill="#28c941"/>')

    # Title
    p.append(f'  <text x="{W//2}" y="{cy2}" text-anchor="middle" fill="{GRAY}" '
             f'font-family="\'Courier New\',monospace" font-size="10" dominant-baseline="middle">'
             f'CHAKRA MONITOR  \u2015  neelashish.sys</text>')

    # Live dot
    p.append(f'  <circle cx="776" cy="{cy2}" r="3.5" fill="{ORANGE}">'
             f'<animate attributeName="opacity" values="1;0.15;1" dur="1.4s" repeatCount="indefinite"/>'
             f'</circle>')

    # Subtle grid
    p.append(f'  <g stroke="{TITLEBAR}" stroke-width="1" opacity="0.8">')
    for gy in [50, 65, 80]:
        p.append(f'    <line x1="0" y1="{gy}" x2="{W}" y2="{gy}"/>')
    for gx in [200, 400, 600]:
        p.append(f'    <line x1="{gx}" y1="{CLIP_TOP}" x2="{gx}" y2="{CLIP_BOT}"/>')
    p.append(f'  </g>')

    # Organic wave — animated scroll
    p.append(f'  <g clip-path="url(#ekgClip)">')
    p.append(f'    <path fill="none" stroke="{GREEN}" stroke-width="2" '
             f'stroke-linecap="round" stroke-linejoin="round" filter="url(#glow)"'
             f' d="{wave_path}">'
             f'<animateTransform attributeName="transform" type="translate" '
             f'from="0,0" to="-800,0" dur="6s" repeatCount="indefinite"/>'
             f'</path>')
    p.append(f'  </g>')

    # Status bar
    p.append(f'  <rect x="0" y="{CLIP_BOT}" width="{W}" height="{H - CLIP_BOT}" fill="{TITLEBAR}"/>')
    p.append(f'  <text y="{H - 4}" font-family="\'Courier New\',monospace" font-size="9">')
    p.append(f'    <tspan x="10"  fill="{GRAY}">SIGNAL: ACTIVE</tspan>')
    p.append(f'    <tspan x="120" fill="{DKGRAY}"> \u2502 </tspan>')
    p.append(f'    <tspan x="130" fill="{GREEN}">STATUS: OPERATIONAL</tspan>')
    p.append(f'    <tspan x="290" fill="{DKGRAY}"> \u2502 </tspan>')
    p.append(f'    <tspan x="300" fill="{ORANGE}">LEVEL: BEGINNER \u2192 HOKAGE</tspan>')
    p.append(f'    <tspan x="510" fill="{DKGRAY}"> \u2502 </tspan>')
    p.append(f'    <tspan x="520" fill="{BLUE}">MISSION: ACTIVE</tspan>')
    p.append(f'  </text>')

    p.append("</svg>")
    return "\n".join(p)


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    print("Fetching GitHub stats...")
    stats = get_github_stats()

    print("Generating terminal.svg...")
    with open("terminal.svg", "w", encoding="utf-8") as f:
        f.write(generate_terminal_svg(stats))

    print("Generating quote.svg...")
    with open("quote.svg", "w", encoding="utf-8") as f:
        f.write(generate_quote_svg())

    print("Generating heartbeat.svg...")
    with open("heartbeat.svg", "w", encoding="utf-8") as f:
        f.write(generate_heartbeat_svg())

    print("Writing README.md...")
    readme = """\
<div align="center">

<table border="0" cellspacing="0" cellpadding="12">
<tr>
<td valign="middle" align="center">
<img src="quote.svg" width="300" alt="Kakashi Quote"/>
</td>
<td valign="top" align="center">
<img src="terminal.svg" width="460" alt="System Info"/>
</td>
</tr>
</table>

<br/>

<img src="heartbeat.svg" width="780" alt="Chakra Monitor"/>

<br/>

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/neelashish-b5a50b380/)
[![X](https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/Neelashish_08)
[![Email](https://img.shields.io/badge/Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:neelashish0@gmail.com)

</div>
"""
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)

    print("[OK] All done!")


if __name__ == "__main__":
    main()
