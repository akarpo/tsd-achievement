"""Shared portable path resolution for all build/extract scripts in Cache and Tools/.

After the 2026-04-28 root-only-output change, generated artifacts (the xlsx and the
dashboard html) live ONLY at the git repo root — there's no canonical copy inside
Cache and Tools/ and no handoff copy in Working Folder/.

Layout this file assumes:

    Achievement/                            ← REPO_ROOT (git repo root)
    ├── index.html                          ← dashboard (the only copy)
    ├── G3-G7_Achievement_Data.xlsx         ← xlsx (the only copy — generated here)
    ├── LICENSE, README.md
    └── Working Folder/                     ← WORKING_FOLDER
        ├── Cache and Tools/                ← HERE  (everything below lives in here)
        │   ├── _paths.py                   (this file)
        │   ├── *.py / rebuild.command      (tooling)
        │   ├── extracted_data/             (input + master CSVs)
        │   ├── source_data/                (raw downloads, mostly MI)
        │   ├── spreadsheets/               (intermediate analytical artifacts)
        │   └── project_docs/               (README, CONVERSATION_SUMMARY, HISTORY_INDEX)
        ├── CHANGELOG.md, README.md
        └── Prompts/                        (per-prompt session capsules)

All scripts resolve everything off __file__, so they're independent of any
absolute path on the host machine — only the relative layout matters.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))            # Working Folder/Cache and Tools/
WORKING_FOLDER = os.path.dirname(HERE)                        # Working Folder/
REPO_ROOT = os.path.dirname(WORKING_FOLDER)                   # Achievement/  (git repo root)

# Data + intermediate outputs live inside HERE (Cache and Tools/).
PROJECT = HERE

EXTRACTED    = os.path.join(PROJECT, 'extracted_data')
SOURCE       = os.path.join(PROJECT, 'source_data')
SPREADSHEETS = os.path.join(PROJECT, 'spreadsheets')
DOCS         = os.path.join(PROJECT, 'project_docs')

# Master CSV + dashboard JSON are intermediate — stay inside Cache and Tools/.
MASTER_CSV     = os.path.join(EXTRACTED, 'master_demographics.csv')
DASHBOARD_JSON = os.path.join(EXTRACTED, 'g3g7_data.json')

# DELIVERABLES — generated artifacts go to REPO ROOT ONLY (no canonical copy elsewhere).
DASHBOARD_XLSX = os.path.join(REPO_ROOT, 'G3-G7_Achievement_Data.xlsx')
DASHBOARD_HTML = os.path.join(REPO_ROOT, 'index.html')

# --- Per-state extracted CSVs (intermediate inputs) ---
CA_DEMO_CSV   = os.path.join(EXTRACTED, 'CA_CAASPP', 'ca_demographics_extracted.csv')
NJ_DEMO_CSV   = os.path.join(EXTRACTED, 'NJ_NJSLA',  'wwp_demographics_2019_2024.csv')
NJ_2425_CSV   = os.path.join(EXTRACTED, 'NJ_NJSLA',  'wwp_2425_demographics.csv')
WA_DEMO_CSV   = os.path.join(EXTRACTED, 'WA_OSPI',   'bellevue_demographics.csv')
TX_DEMO_CSV   = os.path.join(EXTRACTED, 'TX_TAPR',   'coppell_demographics.csv')
MI_TROY_CSV   = os.path.join(EXTRACTED, 'MI_Troy',   'data.csv')

# --- Per-state source data folders (raw downloads — most NOT in repo) ---
SOURCE_NJ_2425    = os.path.join(SOURCE, 'NJ_NJSLA_2425')
SOURCE_CA_CAASPP  = os.path.join(SOURCE, 'CA_CAASPP')
SOURCE_NJ_SPR     = os.path.join(SOURCE, 'NJ_SPR')
SOURCE_TX_TAPR    = os.path.join(SOURCE, 'TX_TAPR')
SOURCE_MI         = os.path.join(SOURCE, 'MI_TSD_Achievement')
