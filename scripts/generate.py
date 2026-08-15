# Generate the DBA-focused Ember Command profile art.

from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
CONFIG = ROOT / "config.json"

BG = "#090708"
SHELL = "#171012"
CORE = "#0f0b0c"
HAIR = "#4b2524"
RED = "#ff4d3d"
ORANGE = "#ff8a1f"
GOLD = "#ffc857"
CREAM = "#fff4e6"
MUTED = "#bda7a2"

DEMO_REPO = {
    "name": "KeySwitchFix",
    "description": "Windows keyboard layout auto-correction utility.",
    "language": "C",
}


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def request_json(url: str) -> object:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "ember-command-profile",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=25) as response:
        return json.load(response)


def live_repo(username: str, featured: list[str]) -> dict:
    repos = request_json(
        f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated"
    )
    if not isinstance(repos, list):
        raise RuntimeError("Unexpected response from GitHub")

    original = [
        repo for repo in repos
        if not repo.get("fork")
        and repo.get("name", "").lower() != username.lower()
    ]
    by_name = {repo.get("name", "").lower(): repo for repo in original}

    for name in featured:
        repo = by_name.get(name.lower())
        if repo:
            return repo

    return original[0] if original else DEMO_REPO


def clip(value: object, length: int) -> str:
    text = " ".join(str(value or "").split())
    return text if len(text) <= length else text[: length - 1].rstrip() + "…"


def hero_svg(config: dict) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="330" viewBox="0 0 900 330" role="img" aria-label="Profile banner for {escape(config["name"])}">
<defs>
  <radialGradient id="flare" cx="78%" cy="42%" r="54%"><stop offset="0" stop-color="{RED}" stop-opacity=".32"/><stop offset=".46" stop-color="{ORANGE}" stop-opacity=".1"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></radialGradient>
  <linearGradient id="rim" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{RED}"/><stop offset=".52" stop-color="{ORANGE}"/><stop offset="1" stop-color="{GOLD}"/></linearGradient>
  <filter id="glow"><feGaussianBlur stdDeviation="7" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <style>.display{{font:700 42px 'Trebuchet MS',sans-serif;fill:{CREAM};letter-spacing:-1.2px}}.label{{font:700 10px 'Trebuchet MS',sans-serif;fill:{ORANGE};letter-spacing:2px}}.body{{font:14px 'Trebuchet MS',sans-serif;fill:{MUTED}}}.hero{{font:700 28px 'Trebuchet MS',sans-serif;fill:{CREAM};letter-spacing:.5px}}.tiny{{font:10px 'Trebuchet MS',sans-serif;fill:{MUTED};letter-spacing:1.2px}}@keyframes drift{{50%{{transform:rotate(7deg)}}}}@keyframes rise{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:translateY(0)}}}}.orbit{{transform-origin:730px 156px;animation:drift 7s cubic-bezier(.32,.72,0,1) infinite}}.intro{{animation:rise .9s cubic-bezier(.32,.72,0,1) both}}@media(prefers-reduced-motion:reduce){{.orbit,.intro{{animation:none}}}}</style>
</defs>
<rect width="900" height="330" rx="26" fill="{SHELL}"/><rect x="7" y="7" width="886" height="316" rx="21" fill="{CORE}" stroke="{HAIR}"/><rect x="7" y="7" width="886" height="316" rx="21" fill="url(#flare)"/>
<path d="M29 41h330" stroke="url(#rim)" stroke-width="2"/><circle cx="29" cy="41" r="4" fill="{RED}"/><text x="42" y="69" class="label">DATABASE COMMAND / PROFILE</text>
<g class="intro"><text x="42" y="130" class="display">{escape(config["name"])}</text><text x="42" y="161" class="body">{escape(config["role"])}</text><text x="42" y="188" class="body">{escape(config["location"])}</text><text x="42" y="239" class="label">SPECIALIZATION</text><text x="42" y="264" class="body">Oracle database operations · reliability · performance</text></g>
<g class="orbit"><circle cx="730" cy="156" r="108" fill="none" stroke="#5d2925"/><circle cx="730" cy="156" r="82" fill="none" stroke="#351919" stroke-dasharray="3 8"/><path d="M635 107a108 108 0 0 1 188 104" fill="none" stroke="url(#rim)" stroke-width="3" stroke-linecap="round"/><circle cx="635" cy="107" r="6" fill="{RED}" filter="url(#glow)"/><circle cx="823" cy="211" r="5" fill="{GOLD}"/></g>
<text x="730" y="147" text-anchor="middle" class="hero">ORACLE DBA</text><text x="730" y="176" text-anchor="middle" class="tiny">HA · DR · PERFORMANCE</text><text x="730" y="201" text-anchor="middle" class="label">DATABASE OPERATIONS</text>
<text x="858" y="318" text-anchor="end" class="tiny">SAM ALIYAN / AUSTRALIA</text>
</svg>'''


def expertise_card(x: int, y: int, title: str, subtitle: str, index: int) -> str:
    accent = [RED, ORANGE, GOLD, RED, ORANGE, GOLD][index]
    return (
        f'<g transform="translate({x} {y})" class="reveal" style="animation-delay:{index * .07:.2f}s">'
        f'<rect width="252" height="76" rx="14" fill="#140e0f" stroke="#4d2523"/>'
        f'<circle cx="20" cy="20" r="4" fill="{accent}"/>'
        f'<text x="34" y="24" class="skill">{escape(title)}</text>'
        f'<text x="20" y="51" class="desc">{escape(subtitle)}</text></g>'
    )


def signal_svg(config: dict, repo: dict) -> str:
    expertise = [
        ("Oracle Database", "Administration · architecture"),
        ("Data Guard", "Standby · switchover · DR"),
        ("Oracle RAC", "Clustered availability"),
        ("RMAN", "Backup · recovery · restore"),
        ("PL/SQL", "Database-side automation"),
        ("Performance Tuning", "SQL · waits · diagnostics"),
    ]
    cards = []
    for index, (title, subtitle) in enumerate(expertise):
        col, row = index % 3, index // 3
        cards.append(expertise_card(31 + col * 272, 92 + row * 96, title, subtitle, index))

    repo_name = clip(repo.get("name") or "KeySwitchFix", 22)
    repo_desc = repo.get("description")
    if not repo_desc and str(repo_name).lower() == "keyswitchfix":
        repo_desc = "Windows keyboard layout auto-correction utility."
    repo_desc = clip(repo_desc or "Public GitHub project", 56)
    language = clip(repo.get("language") or "Mixed", 16)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="390" viewBox="0 0 900 390" role="img" aria-label="Oracle DBA expertise dashboard for {escape(config["username"])}">
<defs><linearGradient id="line"><stop stop-color="{RED}"/><stop offset=".5" stop-color="{ORANGE}"/><stop offset="1" stop-color="{GOLD}"/></linearGradient><style>.title{{font:700 25px 'Trebuchet MS',sans-serif;fill:{CREAM}}}.label{{font:700 9px 'Trebuchet MS',sans-serif;fill:{ORANGE};letter-spacing:1.5px}}.skill{{font:700 13px 'Trebuchet MS',sans-serif;fill:{CREAM}}}.desc{{font:10px 'Trebuchet MS',sans-serif;fill:{MUTED}}}.repo{{font:700 13px 'Trebuchet MS',sans-serif;fill:{CREAM}}}.mono{{font:10px ui-monospace,Consolas,monospace;fill:{MUTED}}}@keyframes reveal{{from{{opacity:0;transform:translateY(5px)}}to{{opacity:1;transform:translateY(0)}}}}.reveal{{animation:reveal .7s cubic-bezier(.32,.72,0,1) both}}@media(prefers-reduced-motion:reduce){{.reveal{{animation:none}}}}</style></defs>
<rect width="900" height="390" rx="26" fill="{SHELL}"/><rect x="7" y="7" width="886" height="376" rx="21" fill="{CORE}" stroke="{HAIR}"/><path d="M29 42h842" stroke="url(#line)"/>
<text x="31" y="39" class="label">CORE EXPERTISE / ORACLE DATABASE ADMINISTRATION</text>
{''.join(cards)}
<text x="31" y="309" class="label">PROJECT SIGNAL</text>
<g transform="translate(31 325)" class="reveal"><rect width="838" height="43" rx="12" fill="#140e0f" stroke="#4d2523"/><circle cx="20" cy="21" r="4" fill="{RED}"/><text x="34" y="19" class="repo">{escape(repo_name)}</text><text x="34" y="34" class="desc">{escape(repo_desc)}</text><text x="810" y="26" text-anchor="end" class="mono">{escape(language)}</text></g>
</svg>'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true", help="use deterministic preview data")
    args = parser.parse_args()

    config = load_config()
    username = (
        os.environ.get("GH_USERNAME")
        or os.environ.get("GITHUB_REPOSITORY_OWNER")
        or config["username"]
    )
    config["username"] = username

    if args.demo:
        repo = DEMO_REPO
    else:
        try:
            repo = live_repo(username, config.get("featured_repos", []))
        except (urllib.error.URLError, RuntimeError) as exc:
            raise SystemExit(
                f"GitHub data request failed: {exc}. Use --demo for an offline preview."
            )

    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "hero.svg").write_text(hero_svg(config), encoding="utf-8")
    (ASSETS / "signal.svg").write_text(signal_svg(config, repo), encoding="utf-8")
    print(f"Generated DBA-focused Ember Command assets for @{username}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
