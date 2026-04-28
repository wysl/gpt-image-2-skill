#!/usr/bin/env python3
from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "generate.py"
FIXED_TEMPLATE = "couple-portrait"
TEMPLATE_DIR = Path(__file__).resolve().parent

HELP = f"""{FIXED_TEMPLATE} template runner

Usage:
  python3 run.py --vars '{{"key":"value"}}' [--output out.png] [--timeout 500]

Routing:
  - template: {FIXED_TEMPLATE}
  - history: {TEMPLATE_DIR / 'history'}
  - output:  {ROOT / 'output'}

Notes:
  - do not pass --template here; this runner fixes it automatically
  - any generated image still lands in the skill-root output directory
"""

args = sys.argv[1:]
if any(a in ('-h', '--help') for a in args):
    print(HELP)
    raise SystemExit(0)
if any(a == "--template" or a.startswith("--template=") for a in args):
    raise SystemExit("This wrapper fixes --template automatically; remove --template from args.")

sys.argv = [str(SCRIPT), "--template", FIXED_TEMPLATE, *args]
runpy.run_path(str(SCRIPT), run_name="__main__")
