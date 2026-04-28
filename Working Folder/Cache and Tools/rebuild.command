#!/bin/bash
# rebuild.command — Regenerate G3-G7_Achievement_Data.xlsx from the corrected
# master_demographics.csv. The xlsx is written directly to the git repo root —
# there's no longer a canonical copy in Cache and Tools/dashboard/ or a handoff
# copy in Working Folder/. The repo root is the only place generated artifacts live.
#
# Lives in:  Working Folder/Cache and Tools/
# Reads:     Cache and Tools/extracted_data/master_demographics.csv
# Writes:    REPO_ROOT/G3-G7_Achievement_Data.xlsx          (the only copy)
#
# Note: index.html is NOT rebuilt by this script — it's a static file at the
# repo root with embedded JSON, edited directly when defaults need to change.
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

echo "[1/2] Ensuring openpyxl is installed..."
python3 -m pip install openpyxl --quiet --break-system-packages 2>/dev/null || \
  python3 -m pip install openpyxl --quiet --user 2>/dev/null || \
  echo "(openpyxl install attempt skipped — assuming it's already available)"

echo "[2/2] Regenerating xlsx directly into repo root..."
python3 "$HERE/build_master_xlsx.py"

echo
echo "Done. The xlsx is now at:"
ls -la "$REPO_ROOT/G3-G7_Achievement_Data.xlsx"
