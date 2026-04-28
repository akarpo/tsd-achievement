"""Re-parse NJSLA 2024-25 bulk Excel for ALL subgroups (race, gender, SWD, ML, ECD).

Lives in: Working Folder/Cache and Tools/
Reads:    achievement_project/source_data/NJ_NJSLA_2425/{ELA,MAT}{03..07}.xlsx
          (raw NJDOE bulk-Excel files — NOT in repo today; download from NJDOE
          and place there before running)
Writes:   achievement_project/extracted_data/NJ_NJSLA/wwp_2425_demographics.csv
"""
import openpyxl, csv, os, sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import SOURCE_NJ_2425, NJ_2425_CSV

DIR = SOURCE_NJ_2425
out_rows = []

# WWP: county=21, district=5715, school=None (district total)
for subj_code, subj in [('ELA','ELA'), ('MAT','Math')]:
    for grade in ['03','04','05','06','07']:
        fn = f'{DIR}/{subj_code}{grade}.xlsx'
        wb = openpyxl.load_workbook(fn, read_only=True, data_only=True)
        ws = wb.active
        for row in ws.iter_rows(min_row=4, values_only=True):
            if row[0] != '21' or row[2] != '5715': continue
            if row[4] is not None and row[4] != '': continue  # skip schools, only district total
            subgroup_type = row[6]
            subgroup = row[7]
            valid = row[10]
            l4 = row[15]
            l5 = row[16]
            try:
                pct = float(l4) + float(l5) if l4 and l5 else None
            except (TypeError, ValueError):
                pct = None
            try:
                valid_n = int(valid) if valid and valid != '*' else None
            except (TypeError, ValueError):
                valid_n = None
            out_rows.append({
                'year': '2025', 'subject': subj, 'grade': grade.lstrip('0'),
                'subgroup_type': subgroup_type, 'subgroup': subgroup,
                'tested': valid_n, 'pct_met': round(pct, 1) if pct else None,
            })

print(f"Extracted {len(out_rows)} rows for 2024-25")
sg_counts = Counter()
for r in out_rows:
    sg_counts[(r['subgroup_type'], r['subgroup'])] += 1
print(f"Distinct subgroups ({len(sg_counts)}):")
for (st, sg), n in sorted(sg_counts.items()):
    print(f"  [{st}] {sg}: {n}")

os.makedirs(os.path.dirname(NJ_2425_CSV), exist_ok=True)
with open(NJ_2425_CSV, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['year','subject','grade','subgroup_type','subgroup','tested','pct_met'])
    w.writeheader()
    w.writerows(out_rows)
print("Saved: wwp_2425_demographics.csv")
