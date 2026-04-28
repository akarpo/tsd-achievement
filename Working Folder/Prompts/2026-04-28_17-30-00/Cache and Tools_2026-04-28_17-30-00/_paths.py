"""Shared portable path resolution for all build/extract scripts in Cache and Tools/.

After the 2026-04-28 consolidation, EVERYTHING the project needs (input CSVs, raw
source files, dashboard outputs, intermediate spreadsheets, project docs) lives
inside this `Cache and Tools/` folder. Scripts resolve everything off __file__,
so they're independent of any absolute path on the host machine — only the
relative layout inside Cache and Tools/ matters.

Layout this file assumes:

    Working Folder/Cache and Tools/        ← HERE
    ├── _paths.py                          (this file)
    ├── *.py / rebuild.command             (tooling)
    ├── extracted_data/                    (input + master CSVs)
    ├── source_data/                       (raw downloads, mostly MI)
    ├── dashboard/                         (canonical build output)
    ├── spreadsheets/                      (intermediate analytical artifacts)
    └── project_docs/                      (README, CONVERSATION_SUMMARY, HISTORY_INDEX)
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))            # Working Folder/Cache and Tools/
WORKING_FOLDER = os.path.dirname(HERE)                        # Working Folder/
REPO_ROOT = os.path.dirname(WORKING_FOLDER)                   # Achievement/  (git repo root)

# Everything is now inside HERE — no more achievement_project hop.
PROJECT = HERE

# --- Top-level project subfolders (all inside Cache and Tools/) ---
EXTRACTED    = os.path.join(PROJECT, 'extracted_data')
SOURCE       = os.path.join(PROJECT, 'source_data')
DASHBOARD    = os.path.join(PROJECT, 'dashboard')
SPREADSHEETS = os.path.join(PROJECT, 'spreadsheets')
DOCS         = os.path.join(PROJECT, 'project_docs')

# --- Master / dashboard outputs ---
MASTER_CSV     = os.path.join(EXTRACTED, 'master_demographics.csv')
DASHBOARD_JSON = os.path.join(EXTRACTED, 'g3g7_data.json')
DASHBOARD_XLSX = os.path.join(DASHBOARD, 'G3-G7_Achievement_Data.xlsx')
DASHBOARD_HTML = os.path.join(DASHBOARD, 'index.html')

# --- Per-state extracted CSVs ---
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

# --- Deploy targets (outside HERE — handoff + GH Pages) ---
HANDOFF_XLSX  = os.path.join(WORKING_FOLDER, 'G3-G7_Achievement_Data.xlsx')
HANDOFF_HTML  = os.path.join(WORKING_FOLDER, 'index.html')
DEPLOY_XLSX   = os.path.join(REPO_ROOT,      'G3-G7_Achievement_Data.xlsx')
DEPLOY_HTML   = os.path.join(REPO_ROOT,      'index.html')
