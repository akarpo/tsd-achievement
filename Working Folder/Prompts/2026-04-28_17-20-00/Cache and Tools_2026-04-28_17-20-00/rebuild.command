#!/bin/bash
# rebuild.command — Regenerate G3-G7_Achievement_Data.xlsx from the corrected
# master_demographics.csv and refresh deployment copies.
#
# Lives in:  Working Folder/Cache and Tools/
# Expects:   Working Folder/achievement_project/  (sibling)
# Updates:   1. achievement_project/dashboard/G3-G7_Achievement_Data.xlsx (canonical)
#            2. Working Folder/{index.html, G3-G7_Achievement_Data.xlsx}    (handoff copies)
#            3. Repo root /index.html and /G3-G7_Achievement_Data.xlsx       (GH Pages deploy)
#
# Double-click in Finder, or invoke from Terminal:
#   bash "rebuild.command"

set -e
HERE="$(cd "$(dirname "$0")" && pwd)"           # Working Folder/Cache and Tools/
WORKING_FOLDER="$(dirname "$HERE")"             # Working Folder/
REPO_ROOT="$(dirname "$WORKING_FOLDER")"        # Achievement/  (git repo root)
ACHIEVEMENT_DIR="$WORKING_FOLDER/achievement_project"

echo "Cache and Tools: $HERE"
echo "Working Folder:  $WORKING_FOLDER"
echo "Repo root:       $REPO_ROOT"
echo "Achievement dir: $ACHIEVEMENT_DIR"
echo

if [ ! -d "$ACHIEVEMENT_DIR" ]; then
  echo "ERROR: $ACHIEVEMENT_DIR not found."
  echo "       This script expects Cache and Tools/ to be a sibling of achievement_project/ inside Working Folder/."
  exit 1
fi

echo "[1/4] Ensuring openpyxl is installed..."
python3 -m pip install openpyxl --quiet --break-system-packages 2>/dev/null || \
  python3 -m pip install openpyxl --quiet --user 2>/dev/null || \
  echo "(openpyxl install attempt skipped — assuming it's already available)"

echo "[2/4] Regenerating G3-G7_Achievement_Data.xlsx from corrected master CSV..."
python3 "$HERE/build_master_xlsx.py"

echo "[3/4] Copying canonical xlsx + dashboard html into Working Folder/ (handoff)..."
cp "$ACHIEVEMENT_DIR/dashboard/index.html"                  "$WORKING_FOLDER/index.html"
cp "$ACHIEVEMENT_DIR/dashboard/G3-G7_Achievement_Data.xlsx" "$WORKING_FOLDER/G3-G7_Achievement_Data.xlsx"

echo "[4/4] Copying canonical xlsx + dashboard html into repo root (GitHub Pages deploy)..."
cp "$ACHIEVEMENT_DIR/dashboard/index.html"                  "$REPO_ROOT/index.html"
cp "$ACHIEVEMENT_DIR/dashboard/G3-G7_Achievement_Data.xlsx" "$REPO_ROOT/G3-G7_Achievement_Data.xlsx"

echo
echo "Done. Three locations now hold the rebuilt artifacts:"
echo "  1. $ACHIEVEMENT_DIR/dashboard/      (canonical source-of-truth)"
echo "  2. $WORKING_FOLDER/                  (handoff copy)"
echo "  3. $REPO_ROOT/                       (GH Pages deploy copy)"
echo
ls -la "$ACHIEVEMENT_DIR/dashboard/G3-G7_Achievement_Data.xlsx" \
       "$WORKING_FOLDER/G3-G7_Achievement_Data.xlsx" \
       "$REPO_ROOT/G3-G7_Achievement_Data.xlsx"
