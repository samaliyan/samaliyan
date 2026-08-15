"""Validate the reviewed static GitHub profile artwork.

The profile SVGs are intentionally hand-tuned.  This script no longer regenerates
visuals from GitHub metrics, because doing so would overwrite the reviewed DBA
layout and featured KeySwitchFix project card.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
REQUIRED = [ASSETS / "hero.svg", ASSETS / "signal.svg", ASSETS / "project.svg"]


def main() -> int:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED if not path.is_file()]
    if missing:
        raise SystemExit("Missing profile assets: " + ", ".join(missing))

    print("Validated reviewed static profile assets: hero.svg, signal.svg, project.svg")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
