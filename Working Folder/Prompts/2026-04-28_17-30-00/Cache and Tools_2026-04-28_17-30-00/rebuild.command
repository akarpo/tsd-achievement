#!/bin/bash
# rebuild.command — Regenerate G3-G7_Achievement_Data.xlsx from the corrected
# master_demographics.csv and refresh deployment copies.
#
# Lives in:  Working Folder/Cache and Tools/   (everything is here now —
#                                                no more achievement_project)
# Updates:   1. Cache and Tools/dashboard/G3-G7_Achievement_Data.xlsx (canonical)
#            2. Working Folder/{index.html, G3-G7_Achievement_Data.xlsx}    (handoff)
#            3. Repo root /index.html and /G3-G7_Achievement_Data.xlsx       (GH Pages)
#
# Double-click in Finder, or invoke from Terminal:
#   bash "rebuild.command"

set -e
HERE="$(cd "$(dirname "$0")" && pwd)"             # Working Folder/Cache and Tools/
WORKING_FOLDER="$(dirname "$HERE")"               # Working Folder/
REPO_ROOT="$(dirname "$WORKING_FOLDER")"          # Achievement/  (git repo root)

echo "Cache and Tools (all data + tools + outputs): $HERE"
echo "Working Folder (handoff target):              $WORKING_FOLDER"
echo "Repo root (GH Pages deploy target):           $REPO_ROOT"
echo

if [ ! -f "$HERE/extracted_data/master_demographics.csv" ]; then
  echo "ERROR: $HERE/extracted_data/master_demographics.csv not found."
  echo "       Cache and Tools/ should contain all data — was it migrated correctly?"
  exit 1
fi

echo "[1/4] Ensuring openpyxl is installed..."
python3 -m pip install openpyxl --quiet --break-system-packages 2>/dev/null || \
  python3 -m pip install openpyxl --quiet --user 2>/dev/null || \
  echo "(openpyxl install attempt skipped — assuming it's already available)"

echo "[2/4] Regenerating canonical xlsx from master CSV..."
python3 "$HERE/build_master_xlsx.py"

echo "[3/4] Copying canonical xlsx + dashboard html into Working Folder/ (handoff)..."
cp "$HERE/dashboard/index.html"                  "$WORKING_FOLDER/index.html"
cp "$HERE/dashboard/G3-G7_Achievement_Data.xlsx" "$WORKING_FOLDER/G3-G7_Achievement_Data.xlsx"

echo "[4/4] Copying canonical xlsx + dashboard html into repo root (GitHub Pages deploy)..."
cp "$HERE/dashboard/index.html"                  "$REPO_ROOT/index.html"
cp "$HERE/dashboard/G3-G7_Achievement_Data.xlsx" "$REPO_ROOT/G3-G7_Achievement_Data.xlsx"

echo
echo "Done. Three locations now hold the rebuilt artifacts:"
echo "  1. $HERE/dashboard/                  (canonical source-of-truth)"
echo "  2. $WORKING_FOLDER/                   (handoff copy)"
echo "  3. $REPO_ROOT/                        (GH Pages deploy copy)"
echo
ls -la "$HERE/dashboard/G3-G7_Achievement_Data.xlsx" \
       "$WORKING_FOLDER/G3-G7_Achievement_Data.xlsx" \
       "$REPO_ROOT/G3-G7_Achievement_Data.xlsx"
