#!/usr/bin/env python3
"""Build world_history_wave20_facts.py"""
from __future__ import annotations
import pprint, re, textwrap
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "world_history_wave20_facts.py"
MIXED = re.compile(r"[\u0D00-\u0D7F][a-zA-Z]|[a-zA-Z][\u0D00-\u0D7F]")
ANATOLIA = "\u0D05\u0D28\u0D3E\u0D1F\u0D4D\u0D30\u0D3E\u0D1F\u0D4B\u0D32\u0D3F\u0D2F"

def clean(rows):
    out = []
    for row in rows:
        if all(not MIXED.search(x) for x in row):
            out.append(row)
        else:
            print("SKIP mixed:", row)
    return out

# --- DATA (pure Malayalam tokens only) ---
CIVILIZATION_REGION = clean([
    ("സുമേർ", "മെസോപൊട്ടാമിയ"), ("ബാബിലോൺ", "മെസോപൊട്ടാമിയ"), ("അസീrir", "മെസോപൊട്ടാമിയ"),
])
