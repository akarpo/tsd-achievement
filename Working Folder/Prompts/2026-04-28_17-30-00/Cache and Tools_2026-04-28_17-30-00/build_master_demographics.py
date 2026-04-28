"""Consolidate all demographic data into a single master CSV.

Lives in: Working Folder/Cache and Tools/
Reads:    achievement_project/extracted_data/{CA,NJ,WA,TX,MI}_*/* CSVs
Writes:   achievement_project/extracted_data/master_demographics.csv

⚠️  AUDIT WARNING — DO NOT RUN BLINDLY ⚠️
The current per-state extracted CSVs in achievement_project/extracted_data/ produce
~5,232 master rows when this script is executed. The CANONICAL master_demographics.csv
checked into the project has 5,917 rows. Running this script will OVERWRITE the canonical
master with a smaller (incomplete) version — the loss is concentrated in the MI Troy
rows, where the original master was sourced from richer CEPI files than what
extracted_data/MI_Troy/data.csv captures (only SWD/Non-SWD/All).

To use this script safely, first reconcile the MI Troy input:
  - Either expand extracted_data/MI_Troy/data.csv to include the additional subgroups
  - Or update this script to read directly from source_data/MI_TSD_Achievement/{year}/
The Bellevue/CA/NJ/TX inputs are fine — only the MI side drifts.

Until that audit is done, prefer:
  - patch_xlsx_in_place.py (surgical edits to existing master + xlsx)
  - Manual edits to extracted_data/master_demographics.csv + ./rebuild.command
"""
import csv, os, sys
from collections import defaultdict, Counter

# Portable path resolution.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import (CA_DEMO_CSV, NJ_DEMO_CSV, NJ_2425_CSV, WA_DEMO_CSV,
                    TX_DEMO_CSV, MI_TROY_CSV, MASTER_CSV)

master = []

def normalize(district, state, file_path, subgroup_col='subgroup', tested_col='tested', pct_col='pct_met'):
    rows = []
    with open(file_path) as f:
        for r in csv.DictReader(f):
            rows.append({
                'district': district, 'state': state,
                'year': r['year'], 'subject': r['subject'], 'grade': str(r['grade']).strip(),
                'subgroup': r[subgroup_col],
                'tested': int(r[tested_col]) if r.get(tested_col) and r[tested_col] not in ('', 'None', None) else None,
                'pct_met': float(r[pct_col]) if r.get(pct_col) and r[pct_col] not in ('', 'None', None) else None,
            })
    return rows

# CA — has district name in the file
with open(CA_DEMO_CSV) as f:
    for r in csv.DictReader(f):
        master.append({
            'district': r['district'], 'state': 'CA',
            'year': r['year'], 'subject': r['subject'], 'grade': r['grade'],
            'subgroup': r['subgroup'],
            'tested': int(r['tested']) if r['tested'] and r['tested'] != '' else None,
            'pct_met': float(r['pct_met']) if r['pct_met'] and r['pct_met'] != '' else None,
        })

# NJ pre-2024-25 (4 years)
master += normalize('West Windsor-Plainsboro', 'NJ', NJ_DEMO_CSV)

# NJ 2024-25 — different schema
with open(NJ_2425_CSV) as f:
    for r in csv.DictReader(f):
        # Normalize subgroup names to match prior years
        sg = r['subgroup']
        sg_map = {
            'All Students': 'All Students', 'White': 'White', 'Hispanic': 'Hispanic',
            'Black or African American': 'Black or African American',
            'Asian': 'Asian/Pacific Islander', 'Native Hawaiian': 'Pacific Islander',
            'American Indian': 'American Indian', 'Other': 'Two or More Races',
            'Female': 'Female', 'Male': 'Male',
            'Students With Disabilities': 'SWD', 'Multilingual Learners': 'Multilingual Learners',
            'Economically Disadvantaged': 'Econ Disadvantaged',
            'Non-Econ. Disadvantaged': 'Not Econ Disadv',
            'Current - Ml': 'Current ML', 'Former - Ml': 'Former ML',
            'SE Accommodation': 'SE Accommodation',
        }
        if sg not in sg_map: continue
        master.append({
            'district': 'West Windsor-Plainsboro', 'state': 'NJ',
            'year': r['year'], 'subject': r['subject'], 'grade': str(r['grade']).lstrip('0'),
            'subgroup': sg_map[sg],
            'tested': int(r['tested']) if r['tested'] and r['tested'] != '' else None,
            'pct_met': float(r['pct_met']) if r['pct_met'] and r['pct_met'] != '' else None,
        })

# WA Bellevue
master += normalize('Bellevue SD', 'WA', WA_DEMO_CSV)

# TX Coppell
master += normalize('Coppell ISD', 'TX', TX_DEMO_CSV)

# MI Troy — read existing data.csv (only SWD/Non-SWD/All)
with open(MI_TROY_CSV) as f:
    for r in csv.DictReader(f):
        sy = r['year']
        spring = '20' + sy.split('-')[1] if len(sy.split('-')[1]) == 2 else sy.split('-')[1]
        try:
            adv_prof = int(r['adv_plus_prof']) if r['adv_plus_prof'] else None
            partial = int(r['n_partial']) if r['n_partial'] else 0
            not_p = int(r['n_not_proficient']) if r['n_not_proficient'] else 0
        except ValueError: continue
        n_tested = (adv_prof or 0) + partial + not_p
        if n_tested == 0: continue
        pct = (adv_prof / n_tested * 100) if adv_prof is not None else None
        master.append({
            'district': 'Troy SD', 'state': 'MI',
            'year': spring, 'subject': r['subject'], 'grade': r['grade'],
            'subgroup': r['group'],  # 'SWD' or 'Non-SWD'
            'tested': n_tested,
            'pct_met': round(pct, 1) if pct is not None else None,
        })

# Filter to G3-G7 only and years of interest
TARGET_YEARS = {'2019', '2022', '2023', '2024', '2025'}
TARGET_GRADES = {'3','4','5','6','7'}
master = [r for r in master if r['year'] in TARGET_YEARS and r['grade'] in TARGET_GRADES]

# Save
out_path = MASTER_CSV
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['district','state','year','subject','grade','subgroup','tested','pct_met'])
    w.writeheader(); w.writerows(master)

print(f"Total master rows: {len(master):,}")
# Coverage by district × subgroup
from collections import defaultdict
cov = defaultdict(set)
for r in master:
    cov[r['district']].add(r['subgroup'])
print(f"\nCoverage by district:")
for d, sgs in sorted(cov.items()):
    print(f"  {d:30s} {len(sgs):>2} subgroups: {', '.join(sorted(sgs))[:120]}")

print(f"\nSaved: {out_path}")
print(f"  Size: {os.path.getsize(out_path)/1024:.0f} KB")
