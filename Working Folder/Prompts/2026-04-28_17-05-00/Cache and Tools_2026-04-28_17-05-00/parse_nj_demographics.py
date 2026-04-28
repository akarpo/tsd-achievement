"""Re-parse NJ SPR PDFs — handle wrapped labels by anchoring on leading text only.

Lives in: Working Folder/Cache and Tools/
Reads:    achievement_project/source_data/NJ_SPR/wwp_district_*.txt
          (text-extracted SPR PDFs — NOT in repo today; pdftotext the raw SPRs)
Writes:   achievement_project/extracted_data/NJ_NJSLA/wwp_demographics_2019_2024.csv
"""
import re, csv, os, sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import SOURCE_NJ_SPR, NJ_DEMO_CSV

YEAR_FILES = {'2019': 'wwp_district_201819.txt', '2022': 'wwp_district_202122.txt',
              '2023': 'wwp_district_202223.txt', '2024': 'wwp_district_202324.txt'}

# (regex_anchor that matches START of label — data follows directly, friendly_name)
SUBGROUP_ANCHORS = [
    (r'Districtwide', 'All Students'),
    (r'White', 'White'),
    (r'Hispanic', 'Hispanic'),
    (r'Black or African American', 'Black or African American'),
    (r'Asian, Native Hawaiian,?\s*or', 'Asian/Pacific Islander'),
    (r'American Indian or Alaska', 'American Indian'),
    (r'Two or More Races', 'Two or More Races'),
    (r'Female', 'Female'),
    (r'Male(?!\s+(?:Test|Teach))', 'Male'),
    (r'Economically Disadvantaged(?!\s*Stud)', 'Econ Disadvantaged'),  # "Economically Disadvantaged" then NEWLINE
    (r'Non-Economically', 'Not Econ Disadv'),
    (r'Students with Disabilities', 'SWD'),
    (r'Students without Disabilities', 'Non-SWD'),
    (r'Multilingual Learners(?!\s*\.)', 'Multilingual Learners'),
    (r'Non-Multilingual Learners', 'Non-ML'),
]

def extract_grade_section(text, subject_label, grade):
    pat = re.compile(re.escape(subject_label) + r'.{0,50}Performance [Bb]y Grade: Grade ' + grade + r'\b', re.IGNORECASE)
    m = pat.search(text)
    if not m: return None
    start = m.end()
    next_m = re.search(r'Performance [Bb]y Grade: Grade', text[start:])
    end = start + next_m.start() if next_m else start + 8000
    return text[start:end]

def parse_subgroup_row(section, anchor_pat):
    # Match anchor + whitespace (incl newlines) + N + 7 fields + final %
    pat = re.compile(anchor_pat + r'\s*[\r\n\s]*(\*|N|\d+(?:,\d+)?)' + r'\s+\S+' * 7 + r'\s+(\*|\d+(?:\.\d+)?%)', re.DOTALL)
    m = pat.search(section)
    if not m: return (None, None)
    n_str = m.group(1).replace(',', '')
    pct_str = m.group(2)
    n = int(n_str) if n_str.isdigit() else None
    pct = None
    if pct_str.endswith('%'):
        try: pct = float(pct_str.rstrip('%'))
        except: pass
    return (n, pct)

base = SOURCE_NJ_SPR
out_rows = []
for year, fn in YEAR_FILES.items():
    path = os.path.join(base, fn)
    if not os.path.exists(path): continue
    with open(path) as f: text = f.read()
    yr_count = 0
    for subj_label, subj_short in [('English Language Arts Assessment', 'ELA'), ('Mathematics Assessment', 'Math')]:
        for grade in ['3', '4', '5', '6', '7']:
            section = extract_grade_section(text, subj_label, grade)
            if not section: continue
            for anchor, friendly in SUBGROUP_ANCHORS:
                n, pct = parse_subgroup_row(section, anchor)
                if n is None and pct is None: continue
                out_rows.append({'year': year, 'subject': subj_short, 'grade': grade,
                                 'subgroup': friendly, 'tested': n, 'pct_met': pct})
                yr_count += 1
    print(f"  {year}: {yr_count} cells")

print(f"\nTotal: {len(out_rows)}")
seen = set(); dedup = []
for r in out_rows:
    k = (r['year'], r['subject'], r['grade'], r['subgroup'])
    if k in seen: continue
    seen.add(k); dedup.append(r)

os.makedirs(os.path.dirname(NJ_DEMO_CSV), exist_ok=True)
with open(NJ_DEMO_CSV, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['year','subject','grade','subgroup','tested','pct_met'])
    w.writeheader(); w.writerows(dedup)

sg_counts = Counter()
for r in dedup: sg_counts[r['subgroup']] += 1
print(f"\nSubgroups ({len(sg_counts)}):")
for sg, n in sorted(sg_counts.items(), key=lambda x: -x[1]):
    print(f"  {sg:30s} {n}")
