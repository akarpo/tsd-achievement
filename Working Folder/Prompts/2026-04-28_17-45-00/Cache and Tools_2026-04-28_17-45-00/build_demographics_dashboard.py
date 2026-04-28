"""Normalize subgroup names + emit JSON for the dashboard.

Lives in: Working Folder/Cache and Tools/
Reads:    achievement_project/extracted_data/master_demographics.csv
Writes:   achievement_project/extracted_data/g3g7_data.json
"""
import csv, json, os, sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import MASTER_CSV, DASHBOARD_JSON

# Subgroup name normalization (canonical names for slicer)
NORM = {
    'All Students': 'All Students',
    'SWD': 'SWD', 'Non-SWD': 'Non-SWD',
    'White': 'White', 'Asian': 'Asian',
    'Asian/Pacific Islander': 'Asian/Pacific Islander', 'Pacific Islander': 'Pacific Islander',
    'Black/African American': 'Black/African American', 'Black or African American': 'Black/African American',
    'Hispanic/Latino': 'Hispanic/Latino', 'Hispanic': 'Hispanic/Latino',
    'American Indian': 'American Indian',
    'Two or More Races': 'Two or More Races',
    'Female': 'Female', 'Male': 'Male',
    'Econ Disadvantaged': 'Econ Disadvantaged', 'Not Econ Disadv': 'Not Econ Disadv',
    'English Learner': 'English Learner', 'English Only': 'English Only',
    'Multilingual Learners': 'Multilingual Learners', 'Current ML': 'Current ML', 'Former ML': 'Former ML',
    'Non-EL': 'Non-EL', 'Non-ML': 'Non-EL',
    'SWD (Former)': 'SWD (Former)',
    'Continuously Enrolled': 'Continuously Enrolled',
    'Non-Continuously Enrolled': 'Non-Continuously Enrolled',
    'Filipino': 'Filipino',
    'SE Accommodation': 'SE Accommodation',
}

# Load and normalize
rows = []
with open(MASTER_CSV) as f:
    for r in csv.DictReader(f):
        sg = NORM.get(r['subgroup'], r['subgroup'])
        rows.append({
            'd': r['district'], 's': r['state'],
            'y': r['year'], 'sub': r['subject'], 'g': r['grade'], 'sg': sg,
            'n': int(r['tested']) if r['tested'] and r['tested'] != '' else None,
            'p': float(r['pct_met']) if r['pct_met'] and r['pct_met'] != '' else None,
        })

# Filter G3-G7 SWD/All to verify
print(f"Master rows after norm: {len(rows):,}")

# Build a compact JSON: rows[] + lookup dicts for districts/subgroups/years
districts = sorted(set(r['d'] for r in rows))
subgroups = sorted(set(r['sg'] for r in rows))
years = sorted(set(r['y'] for r in rows))
print(f"Districts: {len(districts)}, Subgroups: {len(subgroups)}, Years: {len(years)}")

# Compact: arrays indexed by columns
DCOL = {d: i for i, d in enumerate(districts)}
SCOL = {s: i for i, s in enumerate(subgroups)}

compact_rows = []
for r in rows:
    compact_rows.append([DCOL[r['d']], SCOL[r['sg']], r['y'], 'M' if r['sub'] == 'Math' else 'E', int(r['g']), r['n'], r['p']])

# State per district (for tooltips)
district_states = {d: next(r['s'] for r in rows if r['d'] == d) for d in districts}

payload = {
    'districts': districts,
    'states': [district_states[d] for d in districts],
    'subgroups': subgroups,
    'years': years,
    'rows': compact_rows,  # [districtIdx, subgroupIdx, year, subjectCode, grade, n, pct]
}

out_path = DASHBOARD_JSON
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, 'w') as f:
    json.dump(payload, f, separators=(',', ':'))
print(f"\nJSON: {os.path.getsize(out_path)/1024:.0f} KB at {out_path}")
