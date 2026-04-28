"""Re-parse Coppell TAPR PDFs for ALL subgroup columns.

TAPR row layout: 16 columns of percentages
Position: 0=State, 1=R10, 2=District, 3=AfAm, 4=Hispanic, 5=White, 6=AmInd, 7=Asian,
          8=Pacific Islander, 9=Two+, 10=SpEd_C, 11=SpEd_F, 12=Cont, 13=NonCont, 14=EconDis, 15=EBEL

Lives in: Working Folder/Cache and Tools/
Reads:    achievement_project/source_data/TX_TAPR/coppell_tapr_{year}.txt
          (text-extracted TAPR PDFs — NOT in repo today; pdftotext the raw TAPRs)
Writes:   achievement_project/extracted_data/TX_TAPR/coppell_demographics.csv
"""
import re, csv, os, sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import SOURCE_TX_TAPR, TX_DEMO_CSV

YEARS = ['2019', '2022', '2023', '2024', '2025']
GRADES = ['3','4','5','6','7']
SUBJECTS = ['Reading', 'Mathematics']

# Column index → subgroup label
COL_MAP = {
    2:  'All Students',
    3:  'Black/African American',
    4:  'Hispanic/Latino',
    5:  'White',
    6:  'American Indian',
    7:  'Asian',
    8:  'Pacific Islander',
    9:  'Two or More Races',
    10: 'SWD',
    11: 'SWD (Former)',
    12: 'Continuously Enrolled',
    13: 'Non-Continuously Enrolled',
    14: 'Econ Disadvantaged',
    15: 'English Learner',
}

def parse_pct(s):
    s = s.strip()
    if s in ('*','-','**'): return None
    if s.endswith('%'):
        try: return int(s[:-1])
        except: return None
    return None

results = []
for year in YEARS:
    txt_path = os.path.join(SOURCE_TX_TAPR, f'coppell_tapr_{year}.txt')
    if not os.path.exists(txt_path): continue
    with open(txt_path) as f:
        text = f.read()
    yr_count = 0
    for grade in GRADES:
        for subject in SUBJECTS:
            section_start = text.find(f'Grade {grade} {subject}')
            if section_start < 0: continue
            next_grade_match = re.search(r'\nGrade \d', text[section_start+10:])
            section_end = section_start + 10 + (next_grade_match.start() if next_grade_match else 5000)
            section = text[section_start:section_end]
            for m in re.finditer(r'At Meets Grade Level or Above\s+(\d{4})\s+((?:\d{1,3}%|\*|-)(?:\s+(?:\d{1,3}%|\*|-)){15})', section):
                row_year = m.group(1)
                vals = re.findall(r'\d{1,3}%|\*|-', m.group(2))
                if len(vals) != 16: continue
                for col_idx, label in COL_MAP.items():
                    pct = parse_pct(vals[col_idx])
                    if pct is None: continue
                    results.append({
                        'year': row_year,
                        'subject': 'ELA' if subject == 'Reading' else 'Math',
                        'grade': grade,
                        'subgroup': label,
                        'tested': None,  # TAPR doesn't publish tested counts at this level
                        'pct_met': pct,
                    })
                    yr_count += 1
    print(f"  {year}: {yr_count} cells")

# Dedupe (each (year, subj, grade, subgroup) once)
seen = set(); dedup = []
for r in results:
    k = (r['year'], r['subject'], r['grade'], r['subgroup'])
    if k in seen: continue
    seen.add(k); dedup.append(r)

os.makedirs(os.path.dirname(TX_DEMO_CSV), exist_ok=True)
with open(TX_DEMO_CSV, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['year','subject','grade','subgroup','tested','pct_met'])
    w.writeheader(); w.writerows(dedup)

print(f"\nTotal: {len(dedup)}")
sg_counts = Counter()
for r in dedup: sg_counts[r['subgroup']] += 1
for sg, n in sorted(sg_counts.items(), key=lambda x: -x[1]):
    print(f"  {sg:30s} {n}")
