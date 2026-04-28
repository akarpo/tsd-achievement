"""Re-parse CA CAASPP for ALL key subgroups across all 4 districts × all 5 years × G3-G7.

Lives in: Working Folder/Cache and Tools/
Reads:    achievement_project/source_data/CA_CAASPP/sb_ca{year}_all_csv_v{1|4}.zip
          (CAASPP statewide research files — multi-GB; NOT in repo today)
Writes:   achievement_project/extracted_data/CA_CAASPP/ca_demographics_extracted.csv
"""
import csv, zipfile, os, sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import SOURCE_CA_CAASPP, CA_DEMO_CSV

YEARS = ['2019', '2022', '2023', '2024', '2025']
DISTRICTS = {'43-69641': 'Palo Alto USD', '43-73387': 'Milpitas USD',
             '19-73460': 'Walnut Valley USD', '01-75093': 'Dublin USD'}

# Subgroups to extract (Demographic ID code → friendly label)
SUBGROUPS = {
    '1': 'All Students', '001': 'All Students',
    '128': 'SWD', '099': 'Non-SWD', '99': 'Non-SWD',
    '31': 'Econ Disadvantaged', '031': 'Econ Disadvantaged', '111': 'Not Econ Disadv',
    '160': 'English Learner',
    '180': 'English Only',
    '075': 'American Indian', '75': 'American Indian',
    '076': 'Asian', '76': 'Asian',
    '074': 'Black/African American', '74': 'Black/African American',
    '077': 'Filipino', '77': 'Filipino',
    '078': 'Hispanic/Latino', '78': 'Hispanic/Latino',
    '079': 'Pacific Islander', '79': 'Pacific Islander',
    '080': 'White', '80': 'White',
    '144': 'Two or More Races',
    '003': 'Female', '3': 'Female',
    '004': 'Male', '4': 'Male',
}

SCHEMAS = {
    '2019': {'sep': ',', 'q': True, 'county': 0, 'district': 1, 'school': 2, 'subgroup': 5, 'grade': 9, 'test_id': 10, 'tested': 12, 'pct': 16},
    '2022': {'sep': '^', 'q': False, 'county': 0, 'district': 1, 'school': 2, 'subgroup': 5, 'grade': 9, 'test_id': 10, 'tested': 12, 'pct': 16},
    '2023': {'sep': '^', 'q': False, 'county': 0, 'district': 1, 'school': 2, 'subgroup': 5, 'grade': 9, 'test_id': 10, 'tested': 12, 'pct': 16},
    '2024': {'sep': '^', 'q': False, 'county': 0, 'district': 1, 'school': 3, 'subgroup': 10, 'grade': 11, 'test_id': 9, 'tested': 13, 'pct': 20},
    '2025': {'sep': '^', 'q': False, 'county': 0, 'district': 1, 'school': 3, 'subgroup': 10, 'grade': 11, 'test_id': 9, 'tested': 13, 'pct': 20},
}

os.chdir(SOURCE_CA_CAASPP)

results = []
for year in YEARS:
    s = SCHEMAS[year]
    zip_path = f'sb_ca{year}_all_csv_v{4 if year=="2019" else 1}.zip'
    inner = f'sb_ca{year}_all_csv_v{4 if year=="2019" else 1}.txt'
    print(f"  {year}: parsing...", end=' ')
    cnt = 0
    with zipfile.ZipFile(zip_path) as z:
        with z.open(inner) as f:
            for ln, line in enumerate(f):
                if ln == 0: continue
                try: line = line.decode('utf-8', errors='replace').rstrip('\r\n')
                except: continue
                parts = next(csv.reader([line])) if s['q'] else line.split(s['sep'])
                if len(parts) < 25: continue
                school = parts[s['school']].strip('"')
                if school not in ('0000000', '0'): continue
                try:
                    cd_key = f"{int(parts[s['county']]):02d}-{int(parts[s['district']]):05d}"
                except ValueError: continue
                if cd_key not in DISTRICTS: continue
                grade = parts[s['grade']].strip('"')
                if grade not in ('3','4','5','6','7'): continue
                test_id = parts[s['test_id']].strip('"')
                if test_id not in ('1','2'): continue
                subgroup_code = parts[s['subgroup']].strip('"')
                if subgroup_code not in SUBGROUPS: continue
                tested = parts[s['tested']].strip('"').replace('*','').strip()
                pct = parts[s['pct']].strip('"').replace('*','').strip()
                try:
                    tested = int(tested) if tested else None
                    pct = float(pct) if pct else None
                except ValueError:
                    continue
                results.append({
                    'year': year, 'district': DISTRICTS[cd_key], 'subject': 'ELA' if test_id=='1' else 'Math',
                    'grade': grade, 'subgroup_code': subgroup_code, 'subgroup': SUBGROUPS[subgroup_code],
                    'tested': tested, 'pct_met': pct,
                })
                cnt += 1
    print(f"{cnt:,} rows")

# Save
out = CA_DEMO_CSV
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['year','district','subject','grade','subgroup_code','subgroup','tested','pct_met'])
    w.writeheader()
    w.writerows(results)
print(f"\nTotal rows: {len(results):,}")
print(f"Saved: {out}")

# Quick sanity check
from collections import Counter
c = Counter()
for r in results:
    c[(r['district'], r['subgroup'])] += 1
print(f"\nDistinct (district × subgroup) cells: {len(c)}")
print(f"Sample districts × subgroups:")
for (dist, sg), n in sorted(c.items())[:10]:
    print(f"  {dist:25s} {sg:30s} {n} rows")
