# G3-G7 Achievement Comparison Project

Multi-state grade-level achievement comparison with full demographic disaggregation across 8 high-performing suburban districts. Spring 2019 - Spring 2025 (+ partial 2021).

## Districts compared

| District | State | State Test |
|---|---|---|
| Troy SD | MI | M-STEP |
| Palo Alto USD | CA | CAASPP |
| Milpitas USD | CA | CAASPP |
| Walnut Valley USD | CA | CAASPP |
| Dublin USD | CA | CAASPP |
| Coppell ISD | TX | STAAR / TAPR |
| West Windsor-Plainsboro Regional | NJ | NJSLA |
| Bellevue SD | WA | Smarter Balanced |

## Project structure

```
achievement_project/
├── README.md                              ← this file
├── dashboard/                             ← deployable site
│   ├── index.html                         ← interactive dashboard (197 KB, all data inline)
│   └── G3-G7_Achievement_Data.xlsx        ← downloadable workbook (229 KB, 7 sheets)
├── spreadsheets/                          ← intermediate analytical artifacts
│   ├── SPED_MultiYear_G3-G7_Comparison.xlsx
│   ├── SPED_Comparison_FY24.xlsx
│   └── Education_Recovery_Scorecard_Comparison.xlsx
├── extracted_data/                        ← per-state extracted CSVs (post-parsing)
│   ├── master_demographics.csv            ← combined master (5,917 rows)
│   ├── CA_CAASPP/
│   ├── MI_Troy/
│   ├── NJ_NJSLA/
│   ├── TX_TAPR/
│   └── WA_OSPI/
├── source_data/                           ← raw downloads
│   └── MI_TSD_Achievement/                ← 6 years of MI School Data CEPI files
│       ├── 18-19/                         ← 2018-19 school year (Spring 2019)
│       ├── 20-21/                         ← 2020-21 (partial COVID year)
│       ├── 21-22/                         ← 2021-22 (Spring 2022)
│       ├── 22-23/                         ← 2022-23 (Spring 2023)
│       ├── 23-24/                         ← 2023-24 (Spring 2024)
│       └── 24-25/                         ← 2024-25 (Spring 2025)
└── scripts/                               ← reproducibility code
    ├── extract_ca_demographics.py
    ├── parse_nj_demographics.py
    ├── extract_2425_demographics.py       ← NJSLA bulk Excel parser
    ├── refresh_demographics.py            ← WA OSPI Socrata API
    ├── parse_tapr_demographics.py
    ├── build_master_demographics.py       ← combines all per-state CSVs
    ├── build_demographics_dashboard.py    ← emits embedded JSON for dashboard
    └── build_master_xlsx.py               ← builds the downloadable XLSX
```

## Data scope

- **5,917 data points** in master CSV
- **8 districts × 26 demographic subgroup labels × 6 years × 5 grades × 2 subjects**
- **~14 universal subgroups** present in most cells: All Students, SWD, Non-SWD, Asian, White, Black/AA, Hispanic/Latino, Two or More Races, Female, Male, Econ Disadvantaged, Not ECD, English Learner, Non-EL
- Race subgroups Pacific Islander + American Indian: heavily FERPA-suppressed across all districts (small N)

## Cross-state comparability

**ABSOLUTE % NOT directly comparable** — each state uses different proficiency thresholds:
- CA (CAASPP / Smarter Balanced): "Met or Exceeded Standard"
- MI (M-STEP): "Proficient or Advanced"
- TX (STAAR via TAPR): "Meets Grade Level or Above"
- NJ (NJSLA): "Met or Exceeded Expectations" (Levels 4-5)
- WA (SBA): "Met Standard" (Levels 3-4)

**Within-district trends ARE comparable** — that's the right metric for cross-district analysis.

## Data sources (authoritative)

- **MI**: MI School Data CEPI Public Performance files — `source_data/MI_TSD_Achievement/{year}/` — official downloads
- **CA**: CAASPP statewide research files (sb_ca{year}_all_csv) — see `scripts/extract_ca_demographics.py` for download/extraction
- **TX**: TEA Texas Academic Performance Reports (TAPR) PDFs
- **NJ**: NJDOE School Performance Reports + 2024-25 NJSLA bulk Excel files
- **WA**: OSPI Open Data API at data.wa.gov (Socrata datasets, 5 IDs per year)

## Curriculum context

The `dashboard/index.html` includes two appendix tables:
1. **State standards** — links to each state's authoritative ELA + Math learning standards documents
2. **District curriculum adoptions** — Math + ELA programs in use per district with adoption years (sourced from district SARCs, board minutes, BoardDocs)

## Deployment

The dashboard is a single self-contained HTML file (~197 KB) with:
- All data embedded as inline JSON (~150 KB)
- Chart.js loaded from CDN
- No backend, no analytics, no cookies

To publish on GitHub Pages: drop `dashboard/index.html` and `dashboard/G3-G7_Achievement_Data.xlsx` into a public repo, enable Pages on main branch root.

## Methodology notes

- G3-G7 aggregate is **n-weighted** using each grade's tested-student count, except Coppell ISD (TAPR doesn't publish per-grade tested counts; uses simple G3-G7 mean).
- Spring 2020 was canceled nationwide. Spring 2021 had limited admin in MI/CA/NJ/WA. Troy MI 2021 data exists from MI files (partial, atypical conditions).
- Subgroup names normalized: "Black/African American," "Hispanic/Latino," "Asian" labels collapsed to canonical names where state-specific labels differ.
- Cells suppressed where N < 10 (FERPA). Lines have year gaps for small subgroups (American Indian, Pacific Islander).
- WW-P 2018-19 SPR has fewer subgroup rows than later years — race/EL/ECD coverage is thinner.
- WW-P Multilingual Learner sub-categories (Current ML / Former ML) only available in 2024-25 bulk Excel files; not in older SPRs.
- Bellevue WA 2024-25 G3-G5 originally had a field-name issue in OSPI Socrata API extraction; corrected by switching `organizationleveltestedgrade` → `organizationlevel` in the per-year schema config.

## Continuation notes

If reopening this in a new project, the cheapest paths to extend coverage:
1. **Other Michigan years' demographic files** — already covered (5 years)
2. **Other CA districts** — re-run `extract_ca_demographics.py` with new district CDS codes
3. **Trend going forward** — for each new spring testing cycle, drop the new MI CEPI file in a new year folder, re-run the parsing scripts, regenerate the master CSV + dashboard data + XLSX
4. **Disability-type breakdowns (Autism)** — NOT available on public MI School Data dashboard or CEPI files. Would require formal data request to MI CEPI (multi-week turnaround).

Built April 2026.
