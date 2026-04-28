# Cache and Tools — Master Build Tooling

This is the canonical home for every tool used to maintain and update the Achievement project. The build capability here is **independent of the achievement_project folder** — every script resolves paths through `_paths.py`, which walks up from this folder to find `Working Folder/achievement_project/` as a sibling. Move the achievement_project anywhere INSIDE Working Folder and the scripts still find it.

## Layout context

```
Achievement/                                     ← git repo root
├── index.html                                   ← deployed (GH Pages)
├── G3-G7_Achievement_Data.xlsx                  ← deployed (GH Pages)
└── Working Folder/
    ├── achievement_project/                     ← data payload (CSVs, source files, dashboard)
    ├── Cache and Tools/                         ← THIS FOLDER — all build tooling
    │   ├── _paths.py                            ← shared path resolver (start here)
    │   ├── rebuild.command                      ← one-click full rebuild
    │   ├── build_master_xlsx.py                 ← regenerates the xlsx
    │   ├── patch_xlsx_in_place.py               ← surgical xlsx patcher (Bellevue cells)
    │   ├── refresh_demographics.py              ← re-pulls Bellevue from OSPI Socrata
    │   ├── build_master_demographics.py         ← combines per-state CSVs into master
    │   ├── build_demographics_dashboard.py      ← emits compact JSON for dashboard
    │   ├── extract_*.py / parse_*.py            ← per-state source-data extractors
    │   └── README.md                            ← this file
    └── Prompts/                                 ← per-prompt session capsules
```

## Quick start (most common operation: rebuild xlsx after editing master_demographics.csv)

Open Terminal:

```bash
cd "$HOME/Dev/Github/Achievement/Working Folder/Cache and Tools"
chmod +x rebuild.command   # one-time
./rebuild.command
```

After `chmod +x`, you can also double-click `rebuild.command` in Finder. It does:

1. Installs `openpyxl` if missing.
2. Runs `build_master_xlsx.py` → regenerates the xlsx from the master CSV.
3. Copies the rebuilt xlsx + dashboard html into `Working Folder/` (handoff copies).
4. Copies the rebuilt xlsx + dashboard html into the **repo root** (GH Pages deploy).

## Tool inventory

| Tool | What it does | Runs today? |
|---|---|---|
| `_paths.py` | Shared path constants. Imported by every other script. | n/a — library |
| `rebuild.command` | Full rebuild: xlsx → handoff → deploy copies. | ✅ |
| `build_master_xlsx.py` | Reads `master_demographics.csv`, writes 7-sheet `.xlsx`. | ✅ |
| `patch_xlsx_in_place.py` | Surgical patcher — fixes the 26 AIM/SBAC Bellevue cells in an existing xlsx without rebuilding from scratch. | ✅ |
| `refresh_demographics.py` | Hits OSPI Socrata API → rewrites `bellevue_demographics.csv`. Run this when WA publishes a new year's data. | ✅ (needs internet) |
| `build_master_demographics.py` | Combines per-state extracted CSVs → `master_demographics.csv`. | ✅ (all per-state CSVs are in the repo) |
| `build_demographics_dashboard.py` | Reads master CSV, writes compact JSON for the dashboard. | ✅ |
| `extract_ca_demographics.py` | Re-parses CAASPP statewide research zips (~multi-GB). | ⚠ Needs raw CAASPP zips staged at `achievement_project/source_data/CA_CAASPP/` |
| `extract_2425_demographics.py` | Re-parses NJSLA 2024-25 bulk Excel files. | ⚠ Needs `NJ_NJSLA_2425/{ELA,MAT}*.xlsx` staged |
| `parse_nj_demographics.py` | Re-parses NJ SPR text-extracted PDFs (2019-2024). | ⚠ Needs `NJ_SPR/wwp_district_*.txt` staged |
| `parse_tapr_demographics.py` | Re-parses Coppell TAPR text-extracted PDFs. | ⚠ Needs `TX_TAPR/coppell_tapr_*.txt` staged |

The four `⚠`-marked tools depend on raw source files that aren't in the repo today (CAASPP zips are too large to commit, the NJ/TX text files were intermediate from prior parsing). The per-state **extracted** CSVs they produce are already in `extracted_data/`, so the downstream chain (master → xlsx → dashboard) works without them.

## Common operations

**After fixing values in `master_demographics.csv`:**
```bash
./rebuild.command
```

**After re-pulling Bellevue from OSPI:**
```bash
python3 refresh_demographics.py
python3 build_master_demographics.py
./rebuild.command
```

**Surgical xlsx fix without full rebuild:**
```bash
python3 patch_xlsx_in_place.py
```

## Why the path indirection?

Each script starts with:
```python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import ...
```

That makes the script find `_paths.py` in its own folder, regardless of where the user invokes it from. `_paths.py` then resolves `Working Folder/achievement_project/` by walking one level up (to Working Folder/) and then into the achievement_project sibling. So:

- Move the whole repo to a different absolute path → still works.
- Rename `Achievement/` → still works.
- The user opens Terminal in any directory and runs `python3 .../build_master_xlsx.py` → still works.
- The only thing that breaks the resolution is renaming/moving `achievement_project/` to a non-sibling location. If you do that, edit the one PROJECT line in `_paths.py`.
