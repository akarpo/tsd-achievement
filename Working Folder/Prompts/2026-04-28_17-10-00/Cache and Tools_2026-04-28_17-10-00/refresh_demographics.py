"""Refresh Bellevue WA demographics with correct field names per dataset year.

Lives in: Working Folder/Cache and Tools/
Hits:     OSPI Socrata API (data.wa.gov)
Writes:   achievement_project/extracted_data/WA_OSPI/bellevue_demographics.csv
"""
import json, urllib.request, urllib.parse, csv, os, sys, time
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import WA_DEMO_CSV

DISTRICT_CODE = "17405"
GRADES = ["3","4","5","6","7"]
SUBJECTS = ["ELA", "Math"]

# Per-year dataset configs (id, count_field, pct_field, org_level_field)
DATASETS = {
    "2019": {"id": "5y3z-mgxd", "n_field": "count_of_students_expected_to_test_including_previously_passed",
             "pct_field": "percentmetstandard", "org_field": "organizationlevel"},
    "2022": {"id": "v928-8kke", "n_field": "count_of_students_expected_to_test_including_previously_passed",
             "pct_field": "percentmetstandard", "org_field": "organizationlevel"},
    "2023": {"id": "xh7m-utwp", "n_field": "count_of_students_expected_to_test_including_previously_passed",
             "pct_field": "percent_consistent_grade_level_knowledge_and_above", "org_field": "organizationlevel"},
    "2024": {"id": "x73g-mrqp", "n_field": "count_of_students_expected_1",
             "pct_field": "percent_consistent_grade_level_knowledge_and_above", "org_field": "organizationlevel"},
    "2025": {"id": "h5d9-vgwi", "n_field": "count_of_students_expected_1",
             "pct_field": "percent_consistent_grade", "org_field": "organizationlevel"},
}

SUBGROUP_MAP = {
    'All Students': 'All Students',
    'Students with Disabilities': 'SWD', 'Non-Students with Disabilities': 'Non-SWD',
    'Non Students with Disabilities': 'Non-SWD',
    'English Language Learners': 'English Learner',
    'Non English Language Learners': 'Non-EL',
    'Non-English Language Learners': 'Non-EL',
    'Multilingual/English Learners': 'English Learner',
    'Non Multilingual/English Learners': 'Non-EL',
    'Low-Income': 'Econ Disadvantaged', 'Non-Low Income': 'Not Econ Disadv',
    'White': 'White', 'Asian': 'Asian',
    'Black/ African American': 'Black/African American',
    'Hispanic/ Latino of any race(s)': 'Hispanic/Latino',
    'American Indian/ Alaskan Native': 'American Indian',
    'Native Hawaiian/ Other Pacific Islander': 'Pacific Islander',
    'Two or More Races': 'Two or More Races',
    'Female': 'Female', 'Male': 'Male',
}

def fetch(ds_id, params):
    qs = urllib.parse.urlencode(params)
    url = f"https://data.wa.gov/resource/{ds_id}.json?{qs}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def to_float(v):
    if v in (None, "", "NULL", "Suppressed"): return None
    s = str(v).strip().rstrip("%")
    try: return float(s)
    except: return None

def to_int(v):
    if v in (None, "", "NULL", "Suppressed"): return None
    try: return int(float(v))
    except: return None

results = []
for year, cfg in DATASETS.items():
    for grade in GRADES:
        try:
            rows = fetch(cfg["id"], {"districtcode": DISTRICT_CODE, "gradelevel": grade.zfill(2), "$limit": 5000})
        except Exception as e:
            print(f"  {year} G{grade}: FETCH ERROR: {e}")
            continue
        # Filter to district-level rows
        district_rows = [r for r in rows if (r.get(cfg["org_field"]) or '').lower() == 'district']
        # Filter to SBAC (regular Smarter Balanced) only — drop AIM (alternate assessment)
        # rows. AIM rows publish "All Students" / "SWD" district totals with N=11-15 for the
        # ~15 students taking the alt-assessment, which collide with the real SBAC rows in
        # the dedup step below. The bug masqueraded as "Math achievement plummeted" — see
        # 2026-04-28 fix in /running.md.
        district_rows = [r for r in district_rows
                         if (r.get("testadministration") or r.get("test_administration_group") or "").upper() == "SBAC"]
        kept = 0
        for r in district_rows:
            sg_raw = r.get("studentgroup") or ""
            if sg_raw not in SUBGROUP_MAP: continue
            friendly = SUBGROUP_MAP[sg_raw]
            sub = (r.get("testsubject") or r.get("subject") or "").strip()
            if sub == 'English Language Arts': sub = 'ELA'
            elif sub == 'Mathematics': sub = 'Math'
            if sub not in SUBJECTS: continue
            count = to_int(r.get(cfg["n_field"]))
            pct = to_float(r.get(cfg["pct_field"]))
            if count is None and pct is None: continue
            results.append({
                "year": year, "subject": sub, "grade": grade,
                "subgroup": friendly, "tested": count, "pct_met": pct,
            })
            kept += 1
        print(f"  {year} G{grade}: {len(rows)} raw, {len(district_rows)} district-level, {kept} subgroup-matched")

# Dedupe
seen = set(); dedup = []
for r in results:
    k = (r["year"], r["subject"], r["grade"], r["subgroup"])
    if k in seen: continue
    seen.add(k); dedup.append(r)

os.makedirs(os.path.dirname(WA_DEMO_CSV), exist_ok=True)
with open(WA_DEMO_CSV, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['year','subject','grade','subgroup','tested','pct_met'])
    w.writeheader(); w.writerows(dedup)

print(f"\nTotal Bellevue rows: {len(dedup)}")
sg_counts = Counter()
for r in dedup: sg_counts[r['subgroup']] += 1
for sg, n in sorted(sg_counts.items(), key=lambda x: -x[1]):
    print(f"  {sg:30s} {n}")

# Coverage by year
print(f"\nBy year:")
yr_counts = Counter()
for r in dedup: yr_counts[r['year']] += 1
for y in sorted(yr_counts):
    print(f"  {y}: {yr_counts[y]}")
