# Cache and Tools — Single home for everything

After the 2026-04-28 consolidation, this folder is the only place the project's data, tooling, and outputs live. There is no `achievement_project/` anymore. Move this folder anywhere on disk, drop it on another Mac, or rename the parent directories — the build still works because every script resolves paths off `__file__` through `_paths.py`.

## What's in here

```
Cache and Tools/
├── _paths.py                               ← shared portable path resolver
├── rebuild.command                         ← one-click full rebuild
├── README.md                               ← this file
│
├── build_master_xlsx.py                    ← regenerates the xlsx from master CSV
├── patch_xlsx_in_place.py                  ← surgical xlsx patcher (Bellevue cells)
├── refresh_demographics.py                 ← re-pulls Bellevue from OSPI Socrata API
├── build_master_demographics.py            ← combines per-state CSVs into master  ⚠ see audit
├── build_demographics_dashboard.py         ← emits compact JSON for dashboard
├── extract_*.py / parse_*.py               ← per-state source-data extractors
│
├── extracted_data/                         ← input + master CSVs (5,917 rows in master)
│   ├── master_demographics.csv
│   ├── CA_CAASPP/                          (4 districts × 5 years)
│   ├── MI_Troy/
│   ├── NJ_NJSLA/                           (2 schemas: SPRs + 2024-25 bulk)
│   ├── TX_TAPR/
│   └── WA_OSPI/                            (Bellevue, post-AIM/SBAC fix)
│
├── source_data/                            ← raw downloads (only MI is in the repo)
│   └── MI_TSD_Achievement/                 (6 years of CEPI files)
│
├── dashboard/                              ← canonical build outputs
│   ├── index.html                          (interactive dashboard, ~197 KB)
│   └── G3-G7_Achievement_Data.xlsx         (7-sheet workbook, ~229 KB)
│
├── spreadsheets/                           ← intermediate analytical artifacts
│
└── project_docs/                           ← project documentation
    ├── README.md                           (project overview)
    ├── CONVERSATION_SUMMARY.md             (history & rationale)
    └── HISTORY_INDEX.md                    (per-prompt index for session 1)
```

## Outputs flow to three places

`rebuild.command` updates all three on every run:

| Location | Purpose |
|---|---|
| `Cache and Tools/dashboard/`  | canonical (source of truth, what scripts write directly) |
| `Working Folder/`             | handoff copy (for sharing without the whole tooling tree) |
| Repo root (`Achievement/`)    | GitHub Pages deploy copy |

## Quick start

The most common operation: rebuild xlsx after editing `extracted_data/master_demographics.csv`:

```bash
cd "$HOME/Dev/Github/Achievement/Working Folder/Cache and Tools"
chmod +x rebuild.command   # one-time
./rebuild.command
```

## Tool inventory

| Tool | What it does | Runs today? |
|---|---|---|
| `_paths.py` | Shared path constants. Imported by every other script. | n/a — library |
| `rebuild.command` | Full rebuild: xlsx → handoff → deploy copies. | ✅ |
| `build_master_xlsx.py` | Reads `master_demographics.csv`, writes 7-sheet `.xlsx`. | ✅ |
| `patch_xlsx_in_place.py` | Surgical patcher — fixes the 26 AIM/SBAC Bellevue cells in an existing xlsx without rebuilding from scratch. | ✅ |
| `refresh_demographics.py` | Hits OSPI Socrata API → rewrites `bellevue_demographics.csv`. Run this when WA publishes a new year's data. | ✅ (needs internet) |
| `build_master_demographics.py` | Combines per-state extracted CSVs → `master_demographics.csv`. | ⚠ See AUDIT WARNING in script header — produces 5,232 rows vs canonical 5,917. Don't run blindly. |
| `build_demographics_dashboard.py` | Reads master CSV, writes compact JSON for the dashboard. | ✅ |
| `extract_ca_demographics.py` | Re-parses CAASPP statewide research zips (~multi-GB). | ⚠ Needs raw CAASPP zips staged at `source_data/CA_CAASPP/` |
| `extract_2425_demographics.py` | Re-parses NJSLA 2024-25 bulk Excel files. | ⚠ Needs `source_data/NJ_NJSLA_2425/{ELA,MAT}*.xlsx` staged |
| `parse_nj_demographics.py` | Re-parses NJ SPR text-extracted PDFs (2019-2024). | ⚠ Needs `source_data/NJ_SPR/wwp_district_*.txt` staged |
| `parse_tapr_demographics.py` | Re-parses Coppell TAPR text-extracted PDFs. | ⚠ Needs `source_data/TX_TAPR/coppell_tapr_*.txt` staged |

The four `⚠`-marked extraction tools depend on raw source files not in the repo today. The per-state extracted CSVs they would produce are already in `extracted_data/`, so the maintenance chain (master CSV → xlsx → dashboard) works without them.

## Common operations

After fixing values in `extracted_data/master_demographics.csv`:
```bash
./rebuild.command
```

After re-pulling Bellevue from OSPI:
```bash
python3 refresh_demographics.py
# then either edit master CSV by hand OR (with caution) run build_master_demographics.py
./rebuild.command
```

Surgical xlsx fix without full rebuild:
```bash
python3 patch_xlsx_in_place.py
```

## Why portable paths

Every script starts with:
```python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import ...
```

`_paths.py` defines `HERE = os.path.dirname(__file__)` (this folder), `WORKING_FOLDER = parent`, `REPO_ROOT = parent of that`. All input/output paths are computed from those. Nothing is hardcoded to a specific user's machine.

So:
- Move the whole repo to a different absolute path → still works.
- Rename `Achievement/` → still works.
- Run `python3 .../build_master_xlsx.py` from any cwd → still works.

The only thing that breaks resolution is moving things INSIDE Cache and Tools/ to non-default subfolders. If you do that, edit the corresponding constant in `_paths.py`.
