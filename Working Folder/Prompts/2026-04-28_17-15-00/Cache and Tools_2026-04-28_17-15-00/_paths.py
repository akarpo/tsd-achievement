"""Shared portable path resolution for all build/extract scripts in Cache and Tools/.

Scripts here resolve the achievement_project/ payload at:
    Working Folder/achievement_project/

regardless of where the user ran them from, by walking up from this file's location.
This is what makes the build capability INDEPENDENT of the achievement_project folder
being at any specific absolute path — only the relative layout matters.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))                  # Working Folder/Cache and Tools/
WORKING_FOLDER = os.path.dirname(HERE)                              # Working Folder/
PROJECT = os.path.join(WORKING_FOLDER, 'achievement_project')       # Working Folder/achievement_project/

# --- Top-level project subfolders ---
EXTRACTED = os.path.join(PROJECT, 'extracted_data')
SOURCE = os.path.join(PROJECT, 'source_data')
DASHBOARD = os.path.join(PROJECT, 'dashboard')
SPREADSHEETS = os.path.join(PROJECT, 'spreadsheets')

# --- Master / dashboard outputs ---
MASTER_CSV = os.path.join(EXTRACTED, 'master_demographics.csv')
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
