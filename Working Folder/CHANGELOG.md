# CHANGELOG — 2026-04-28 Bellevue Fix Session

## Root cause

OSPI's Socrata datasets publish **two** District-level rows for the same `(year, subject, grade, studentgroup)` cell at certain Bellevue grades:
- SBAC row (Smarter Balanced — the regular assessment, N≈1,300-1,500)
- AIM row (alternate assessment for ~11-15 students with significant cognitive disabilities)

`scripts/refresh_demographics.py` deduped on `(year, subject, grade, subgroup)` without distinguishing test administration, so whichever row arrived first won. AIM happened to sort first in 2022, 2024, and 2025 → 26 cells got the AIM values masquerading as district totals.

## Patches applied

### 26 data cells corrected

Format: `year subject grade subgroup` — was → now (N, %)

**2025 (14 cells)** — confirmed against `data.wa.gov/resource/h5d9-vgwi.json`:
- 2025 Math G3 All Students: 15 / 40.0% → 1,345 / 69.4%
- 2025 ELA G3 All Students: 15 / 46.7% → 1,333 / 65.1%
- 2025 ELA G3 SWD: 15 / 46.7% → 170 / 34.7%
- 2025 Math G3 SWD: 15 / 40.0% → 170 / 40.0%
- 2025 Math G4 All Students: 14 / 50.0% → 1,381 / 72.9%
- 2025 ELA G4 SWD: 14 / 64.3% → 175 / 40.0%
- 2025 Math G4 SWD: 14 / 50.0% → 176 / 37.5%
- 2025 Math G5 All Students: 11 / 45.5% → 1,335 / 67.9%
- 2025 ELA G5 SWD: 11 / 36.4% → 139 / 28.1%
- 2025 Math G6 All Students: 11 / 36.4% → 1,486 / 65.3%
- 2025 ELA G6 SWD: 11 / 36.4% → 159 / 22.0%
- 2025 Math G6 SWD: 11 / 36.4% → 159 / 25.2%
- 2025 Math G7 All Students: 11 / 72.7% → 1,502 / 65.3%
- 2025 Math G7 SWD: 11 / 72.7% → 136 / 18.4%

**2024 (4 cells)** — confirmed against `data.wa.gov/resource/x73g-mrqp.json`:
- 2024 Math G4 All Students: 13 / 30.8% → 1,271 / 71.5%
- 2024 Math G4 SWD: 13 / 30.8% → 148 / 32.4%
- 2024 Math G5 All Students: 12 / 66.7% → 1,347 / 67.6%
- 2024 Math G5 SWD: 12 / 66.7% → 161 / 29.2%

**2022 (8 cells)** — confirmed against `data.wa.gov/resource/v928-8kke.json`:
- 2022 ELA G3 All Students: 14 / 28.6% → 1,299 / 71.6%
- 2022 ELA G3 SWD: 14 / 28.6% → 120 / 31.7%
- 2022 Math G3 All Students: 14 / 35.7% → 1,309 / 72.8%
- 2022 Math G3 SWD: 14 / 35.7% → 121 / 34.7%
- 2022 ELA G6 All Students: 11 / 45.5% → 1,391 / 63.8%
- 2022 ELA G6 SWD: 11 / 45.5% → 140 / 15.7%
- 2022 Math G6 All Students: 11 / 36.4% → 1,400 / 61.2%
- 2022 Math G6 SWD: 11 / 36.4% → 140 / 16.4%

### Files modified

- `extracted_data/WA_OSPI/bellevue_demographics.csv` — 26 row replacements
- `extracted_data/master_demographics.csv` — 26 row replacements (same cells)
- `dashboard/index.html` — 26 row replacements in the embedded compact-JSON, plus xlsx download link added in the header
- `scripts/refresh_demographics.py` — added SBAC filter to prevent recurrence:
  ```python
  district_rows = [r for r in district_rows
                   if (r.get("testadministration") or r.get("test_administration_group") or "").upper() == "SBAC"]
  ```
- `scripts/build_master_xlsx.py` — replaced hardcoded sandbox paths (`/sessions/wizardly-dazzling-tesla/mnt/...`) with portable relative paths so the script can be re-run on any machine.

### Files NOT yet updated

- `dashboard/G3-G7_Achievement_Data.xlsx` — still has the AIM-contaminated values until you run `rebuild.command` or `patch_xlsx_in_place.py`.

## Verification

After rebuild, you can spot-check any corrected cell by querying OSPI directly. Example for 2025 Math G3 Bellevue All Students:

```bash
curl -s "https://data.wa.gov/resource/h5d9-vgwi.json?districtcode=17405&organizationlevel=District&testadministration=SBAC&testsubject=Math&gradelevel=03&studentgroup=All%20Students" | python3 -m json.tool
```

Should return `count_of_students_expected_1: "1345"`, `percent_consistent_grade: "69.4%"`.

---

# 2026-04-28 — Session 2 — Dev/Github restructure

User moved the working copy of the project from OneDrive to `/Users/Alex/Dev/Github/Achievement` (a local git repo) to escape OneDrive sync-agent locks. Then restructured the project so build tooling lives outside the data payload, with per-prompt traceability.

## New layout

```
Achievement/                                     (git repo root)
├── index.html                                   (rebuilt — GH Pages deploy)
├── G3-G7_Achievement_Data.xlsx                  (rebuilt — GH Pages deploy)
└── Working Folder/
    ├── achievement_project/                     (moved in from repo root)
    ├── Cache and Tools/                         (NEW — master tooling)
    │   ├── _paths.py                            (NEW — shared portable path resolver)
    │   ├── rebuild.command                      (rewritten for new layout)
    │   ├── build_master_xlsx.py                 (patched — uses _paths)
    │   ├── patch_xlsx_in_place.py
    │   ├── refresh_demographics.py              (patched — uses _paths)
    │   ├── build_master_demographics.py         (patched + audit warning)
    │   ├── build_demographics_dashboard.py      (patched — uses _paths)
    │   ├── extract_*.py / parse_*.py            (patched — uses _paths)
    │   └── README.md                            (NEW — full inventory)
    ├── Prompts/                                 (NEW — per-prompt capsules)
    │   ├── 2026-04-28_14-02-11/  …  16-31-50/  (session 1, retro-folded)
    │   ├── 2026-04-28_17-00-01/  …  17-20-00/  (session 2, with snapshots)
    │   └── running.md                            (chronological session log)
    ├── README.md
    ├── CHANGELOG.md                             (this file)
    ├── G3-G7_Achievement_Data.xlsx              (handoff copy)
    ├── index.html                               (handoff copy)
    ├── _OLD_JUNK_DELETE_ME/                     (sandbox can't unlink locked .DS_Store)
    └── _PYCACHE_DELETE_ME/                      (same)
```

## What changed

1. **`achievement_project/` moved into `Working Folder/`** — was a sibling of Working Folder, now nested inside it.
2. **All scripts moved to `Working Folder/Cache and Tools/`** with portable path resolution via shared `_paths.py`. Every `/sessions/wizardly-dazzling-tesla/mnt/outputs/...` reference replaced with constants resolved relative to the script's own location.
3. **`rebuild.command` rewritten** — now updates three locations on every run:
   - Canonical: `Working Folder/achievement_project/dashboard/`
   - Handoff: `Working Folder/`
   - Deploy: repo root `/`
4. **All historical `.md` prompts retro-folded** into `Working Folder/Prompts/{timestamp}/` capsules.
5. **Per-prompt snapshots** of `Cache and Tools/` added under each session-2 capsule (frozen tooling state at that moment).
6. **xlsx rebuilt** — verified Bellevue 2025 G3 Math All Students = N=1,345, 69.4% across all three deploy locations (identical hashes).

## Self-inflicted regression and recovery (worth flagging for next time)

Mid-restructure, I ran a `for f in *.py; python3 -c "...exec_module..."` loop intending it as an "import sanity check". `exec_module` actually runs the script's top-level code — so `build_master_demographics.py` ran, silently overwriting `master_demographics.csv` with a 5,232-row reduced version (canonical is 5,917 rows). Recovered by copying the canonical master from the OneDrive backup at `/Users/Alex/Library/CloudStorage/OneDrive-Personal/Documents/Claude/Projects/Achievement/`. Then re-ran `rebuild.command`. Added `⚠ AUDIT WARNING` header to `build_master_demographics.py` so it isn't run blindly until the MI Troy input divergence is reconciled.

For future "import-only" checks: use `compile(open(f).read(), f, 'exec')` for syntax validation, not `importlib.util.exec_module`.

## What's left for the user

- Delete `Working Folder/_OLD_JUNK_DELETE_ME/` via Finder (locked `.DS_Store` files prevented sandbox unlink).
- Delete `Working Folder/Cache and Tools/_PYCACHE_DELETE_ME/` (same reason).
- `achievement_project/scripts/` — original (pre-port) script copies still there. Redundant with `Cache and Tools/`. Safe to delete; left in place to avoid breaking unknown external references.
- Reconcile `build_master_demographics.py` MI-Troy input drift (or leave — `rebuild.command` doesn't depend on it; only `patch_xlsx_in_place.py` and `build_master_xlsx.py` are needed for normal maintenance).
- Decide what to commit. The git repo currently has all of this restructure as untracked changes; no commits made.

---

# 2026-04-28 — Session 2.5 — Consolidation into Cache and Tools/

User asked to validate OneDrive independence and asked whether `achievement_project/` could be deleted with all work happening inside `Cache and Tools/`.

## OneDrive validation

Source-code grep across Cache and Tools/ returned ZERO references to OneDrive/CloudStorage/`/Users/Alex/Library`/`/Users/`. Every file I/O resolves through `_paths.py` constants computed off `__file__`. The only sandbox-tied artifact is Python's bytecode cache in `__pycache__/` — regenerated fresh per run, not a runtime dependency.

## Consolidation actions

1. **Moved data into Cache and Tools/:**
   - `achievement_project/extracted_data/` → `Cache and Tools/extracted_data/`
   - `achievement_project/source_data/` → `Cache and Tools/source_data/`
   - `achievement_project/dashboard/` → `Cache and Tools/dashboard/`
   - `achievement_project/spreadsheets/` → `Cache and Tools/spreadsheets/`
2. **Moved project docs:**
   - `achievement_project/{README, CONVERSATION_SUMMARY, HISTORY_INDEX}.md` → `Cache and Tools/project_docs/`
3. **Removed redundant scripts:** `achievement_project/scripts/` (pre-port copies of build scripts, redundant with canonical Cache and Tools/) renamed to `_PRE_PORT_SCRIPTS_DELETE_ME/`.
4. **Rewrote `_paths.py`:** `PROJECT = HERE` (Cache and Tools/ itself). Added `HANDOFF_XLSX/HANDOFF_HTML` (Working Folder/) and `DEPLOY_XLSX/DEPLOY_HTML` (repo root) constants for the three-target deploy flow.
5. **Rewrote `rebuild.command`:** canonical dashboard now at `HERE/dashboard/`; the script computes WORKING_FOLDER and REPO_ROOT by walking up from HERE.
6. **Rewrote `Cache and Tools/README.md`** for the consolidated structure.

## Final layout

```
Achievement/                            (git repo root)
├── index.html                          (GH Pages deploy)
├── G3-G7_Achievement_Data.xlsx         (GH Pages deploy)
└── Working Folder/
    ├── G3-G7_Achievement_Data.xlsx     (handoff copy)
    ├── index.html                      (handoff copy)
    ├── README.md, CHANGELOG.md
    ├── Cache and Tools/                ← EVERYTHING LIVES HERE
    │   ├── _paths.py, rebuild.command, README.md
    │   ├── *.py (10 scripts)
    │   ├── extracted_data/             (input + master CSVs)
    │   ├── source_data/                (raw downloads, MI only in repo)
    │   ├── dashboard/                  (canonical outputs)
    │   ├── spreadsheets/               (intermediate analytical artifacts)
    │   └── project_docs/               (README, CONVERSATION_SUMMARY, HISTORY_INDEX)
    └── Prompts/                        (19 capsules)
```

## Verification

End-to-end rebuild from the new self-contained Cache and Tools/:
- Identical xlsx hash `a77d4426733580d76556d8425d61bfb2` across canonical (Cache and Tools/dashboard/), handoff (Working Folder/), and deploy (repo root).
- All Demographics: 5,497 rows.
- Bellevue 2025 G3 Math All Students = N=1,345, 69.4% (the corrected SBAC value, confirmed preserved through the consolidation).

## Cleanup left for user (Finder)

`rm -rf` couldn't unlink macOS-locked `.DS_Store` and `.pyc` files in the sandbox; renamed to clearly-marked junk folders:

- `Working Folder/_ACHIEVEMENT_PROJECT_DELETE_ME/` (the now-emptied original)
- `Working Folder/Cache and Tools/_PYCACHE_DELETE_ME/` (stale bytecode from earlier in session 2)
- `Working Folder/Cache and Tools/_PYCACHE_NEW_DELETE_ME/` (bytecode from today's rebuild)
- `Working Folder/_OLD_JUNK_DELETE_ME/` (still left from session 2)

Recommend adding `__pycache__/` to `.gitignore` before any commit.

---

# 2026-04-28 — Session 2.6 — Root-only output + dashboard defaults

User asked to (a) change the build so generated files land at the git repo root only, not in Cache and Tools/, and (b) update `index.html` defaults to select all 8 districts and only the "All Students" subgroup.

## Build process change

- `_paths.py`: `DASHBOARD_XLSX` and `DASHBOARD_HTML` now resolve to `REPO_ROOT/`. The `DASHBOARD` constant (pointing at the old `Cache and Tools/dashboard/`) is gone.
- Canonical xlsx + html moved out of `Cache and Tools/dashboard/` to repo root, overwriting the deploy copies. Empty `dashboard/` renamed to `_DASHBOARD_DELETE_ME/` (sandbox couldn't `rmdir` it due to a residual `.DS_Store`).
- `Working Folder/index.html` and `Working Folder/G3-G7_Achievement_Data.xlsx` (handoff copies) removed — renamed to `_index_html_DELETE_ME` and `_xlsx_DELETE_ME` because of the same macOS lock issue.
- `rebuild.command` rewritten — two steps now (install openpyxl, run `build_master_xlsx.py`). No copy step. The script writes directly to the repo root because `_paths.DASHBOARD_XLSX` now points there.
- `build_master_xlsx.py` and `patch_xlsx_in_place.py` needed no edits — both import `DASHBOARD_XLSX` from `_paths`, so they retarget automatically.
- `Cache and Tools/README.md` rewritten with the new "root is the only output location" wording and updated tree.

## index.html defaults

Edited lines 165-166:
```javascript
// Before
selectedDistricts: new Set(['Troy SD', 'Bellevue SD', 'Coppell ISD']),
selectedSubgroups: new Set(['All Students', 'SWD']),

// After
selectedDistricts: new Set(['Bellevue SD', 'Coppell ISD', 'Dublin USD', 'Milpitas USD', 'Palo Alto USD', 'Troy SD', 'Walnut Valley USD', 'West Windsor-Plainsboro']),
selectedSubgroups: new Set(['All Students']),
```

The 8 district names match the embedded data payload exactly (alphabetical order; the order doesn't matter for the Set, but matching the source array makes future audits easier).

## Verification

- Renamed root xlsx to `.before`, ran `rebuild.command`, confirmed fresh write to repo root (new mtime + new MD5 — xlsx contains a creation timestamp so the hash differs even when content is identical).
- All Demographics: 5,497 rows. Bellevue 2025 G3 Math All Students = N=1,345, 69.4% (corrected SBAC value, preserved).
- `find . -name "G3-G7_Achievement_Data.xlsx" -not -path '*_DELETE_ME*' -not -path '*/Prompts/*'` returns exactly one path: `./G3-G7_Achievement_Data.xlsx`. Same for `index.html` — only at repo root.

## Cleanup queue (Finder)

In addition to the prior session's leftovers (`_ACHIEVEMENT_PROJECT_DELETE_ME/`, `_OLD_JUNK_DELETE_ME/`, `_PYCACHE_*_DELETE_ME/`), session 2.6 added:

- `Working Folder/_index_html_DELETE_ME` (the handoff index.html)
- `Working Folder/_xlsx_DELETE_ME` (the handoff xlsx)
- `Working Folder/Cache and Tools/_DASHBOARD_DELETE_ME/` (the empty canonical folder)
- `_BEFORE_REBUILD_xlsx_DELETE_ME` at repo root (the build-verification staging file)

---

# 2026-04-28 — Session 2.7 — Repo-root README removal

User asked to delete the repo-root README.md (initially mis-said "CHANGELOG.md", corrected to "README.md" in the next prompt). The file was a 31-byte placeholder (`# Achievement\nAchievement Data\n`) tracked in the initial git commit.

## Action

- Removed `/Users/Alex/Dev/Github/Achievement/README.md` from the working tree. Sandbox couldn't `rm` due to the macOS-lock issue (same as `.DS_Store`/`.pyc` files all session); renamed to `_README_DELETE_ME` instead. Git records the deletion (`D README.md` in `git status`) which is what matters semantically; the renamed file at root is cosmetic Finder cleanup.
- Verified per-prompt snapshot inclusion was already in place — every existing session-2 capsule has a `Cache and Tools_{ts}/README.md` (the tooling README), and the snapshot-build pattern continues copying it on each new capsule.

## What was NOT touched

- `Working Folder/README.md`
- `Working Folder/Cache and Tools/README.md` (the master that gets snapshotted)
- `Working Folder/Cache and Tools/project_docs/README.md` (the original project overview, archival)

User can request additional removals if needed.

## Cleanup queue addition

- `_README_DELETE_ME` at repo root (in addition to all prior `_*_DELETE_ME` entries)
