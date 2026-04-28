#!/bin/bash
# rebuild.command — Regenerate both deliverables from the corrected
# master_demographics.csv. Both artifacts are written directly to the git repo
# root — there is no canonical copy in Cache and Tools/ and no handoff copy in
# Working Folder/. The repo root is the only place generated artifacts live.
#
# Lives in:  Working Folder/Cache and Tools/
# Reads:     Cache and Tools/extracted_data/master_demographics.csv
# Writes:    REPO_ROOT/G3-G7_Achievement_Data.xlsx
#            REPO_ROOT/index.html  (in place — only the embedded JSON payload changes;
#                                   CSS / JS / slicer defaults are preserved)
#
# Pipeline:
#   1. build_master_xlsx.py             master CSV → xlsx
#   2. build_demographics_dashboard.py  master CSV → extracted_data/g3g7_data.json
#   3. update_index_html.py             g3g7_data.json → embedded payload in index.html
#
# Double-click in Finder, or invoke from Terminal:
#   bash "rebuild.command"

set -e
HERE="$(cd "$(dirname "$0")" && pwd)"             # Working Folder/Cache and Tools/
WORKING_FOLDER="$(dirname "$HERE")"               # Working Folder/
REPO_ROOT="$(dirname "$WORKING_FOLDER")"          # Achievement/  (git repo root)

echo "Cache and Tools (data + tooling): $HERE"
echo "Repo root (output target):        $REPO_ROOT"
echo

if [ ! -f "$HERE/extracted_data/master_demographics.csv" ]; then
  echo "ERROR: $HERE/extracted_data/master_demographics.csv not found."
  exit 1
fi

echo "[1/4] Ensuring openpyxl is installed..."
python3 -m pip install openpyxl --quiet --break-system-packages 2>/dev/null || \
  python3 -m pip install openpyxl --quiet --user 2>/dev/null || \
  echo "(openpyxl install attempt skipped — assuming it's already available)"

echo "[2/4] Regenerating xlsx into repo root..."
python3 "$HERE/build_master_xlsx.py"

echo "[3/4] Rebuilding dashboard JSON from master CSV..."
python3 "$HERE/build_demographics_dashboard.py"

echo "[4/4] Updating embedded payload in index.html..."
python3 "$HERE/update_index_html.py"

echo
echo "Done. Deliverables at repo root:"
ls -la "$REPO_ROOT/G3-G7_Achievement_Data.xlsx" "$REPO_ROOT/index.html"
