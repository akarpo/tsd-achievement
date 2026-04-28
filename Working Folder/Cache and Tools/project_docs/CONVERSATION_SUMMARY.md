# Conversation Summary — Achievement Project

Reference for picking up where this work left off in a new project.

## Where this started

User (Alex) is a parent / community member analyzing **Troy School District (MI)** academic outcomes. Original question: how is Troy doing on Special Education achievement vs. peer high-performing suburban districts? Project evolved into broader G3-G7 achievement comparison with full demographic disaggregation.

## How peer districts were selected

Started with 6 peers from the **Education Recovery Scorecard** (Stanford CEPR / Harvard) — districts with similar SES + Asian-plurality demographics:
- Palo Alto USD (CA)
- Milpitas USD (CA)
- Walnut Valley USD (CA)
- Dublin USD (CA)
- Coppell ISD (TX)
- West Windsor-Plainsboro Regional (NJ)

**Bellevue SD (WA)** added later — discovered to use Illustrative Mathematics K-12 with structural compaction at MS, similar enrollment scale to Troy.

**Birmingham MI (Michigan SD)** also identified as a structural twin to Troy (same Imagine IM curriculum + opt-in compaction, same M-STEP test). Performance data not yet pulled for Birmingham — would be a clean next-step.

## Key data sources consulted

| Source | Purpose | Files in project |
|---|---|---|
| MI School Data CEPI Public Performance | Troy authoritative demographics | `source_data/MI_TSD_Achievement/{year}/` (6 years) |
| CAASPP statewide research files | CA districts demographics | `scripts/extract_ca_demographics.py` (downloads via URL) |
| TEA TAPR PDFs | Coppell demographics | manually downloaded, parsed via regex |
| NJDOE School Performance Reports | WW-P pre-2025 demographics | parsed PDFs |
| NJDOE 2024-25 bulk NJSLA Excel | WW-P 2025 demographics | per-grade Excel files |
| OSPI Socrata API (data.wa.gov) | Bellevue demographics | 5 dataset IDs per year |
| SEDA 2024.3 | Initially considered, RULED OUT | only race/gender/ECD subgroups, no SWD, no race × SWD cross-tab |

## Key findings (worth carrying forward)

1. **Bridges in Math (K-5) appears to advantage SWD students more than gen-ed peers.** Troy adopted Bridges in 2023; SWD Math gained +7.3 pp at G3-G5 (2019→2025) while non-SWD only gained ~1 pp. Pattern holds at PAUSD (Bridges since 2017, SWD Math 38.7%).

2. **Troy Math SWD is the only positive-trending dimension in the entire cohort** at G3-G7 aggregate — +3.8 pp since 2019 (n-weighted). All other districts lost ground on SWD Math; most lost 3-7 pp.

3. **Coppell ISD ELA SWD gained +9.8 pp** since 2019 — the standout positive trend. NOT attributable to a curriculum adoption — Coppell uses NO commercial ELA program, only district-built balanced literacy. Implementation rigor (PD investment, intervention infrastructure) appears more important than curriculum brand.

4. **Bellevue's IM advantage at G6-G7 is largely a curricular-compression artifact.** Bellevue's standard pathway is +1yr compressed (IMT1 covers G6+G7 standards in one year). Apples-to-apples at G3-G5 (where both Troy and Bellevue use on-grade pacing): Troy +7.3 vs Bellevue −1.3 pp on SWD Math since 2019.

5. **Troy has the SMALLEST within-district Asian-Hispanic gap** in the cohort (+29 pp vs +37-58 pp for peers) — relatively more equitable racial outcomes, though Troy Hispanic enrollment is small.

6. **Troy White students gained while peers lost.** Troy White Math +3.4 pp (2019→2025). WW-P −8.0, Bellevue −9.1, Walnut Valley −2.9, Dublin −3.1. Bridges adoption appears to have helped White students recover from COVID more than at peers.

7. **Troy Econ-Disadvantaged students show massive gains.** ECD Math G3 went 41.2% (2019) → 58.7% (2025), a +17.5 pp improvement. ECD-vs-Not gap closed by ~16 pp at G3.

## Curriculum landscape (mapped per district)

See `dashboard/index.html` Appendix tables OR `dashboard/G3-G7_Achievement_Data.xlsx` "Curriculum Adoptions" sheet for full matrix.

Key observations:
- **Bridges in Math adopted by Troy (2023) + Palo Alto (2017)** — both districts trend well on SWD Math
- **Imagine IM adopted by Troy (2023, 6-8) + Bellevue (2021-22, K-12) + Birmingham (2023-24, K-8)** — Imagine IM cohort
- **Calkins/Units of Study** used by Troy + WW-P + Dublin (as supplement) for ELA — all three under pressure to move off Calkins under science-of-reading mandates
- **Coppell + WW-P + Bellevue 6-8** all use district-built ELA (no commercial program). Coppell trending up, WW-P trending sharply down — implementation difference, not curriculum.

## Acceleration pathway research (per district, available in dashboard appendix)

- Troy: ON-GRADE default, no acceleration at MS
- Palo Alto + Bellevue: COMPACTED-by-DEFAULT at G6-G7
- Birmingham: OPT-IN compaction (parallel pathways) — interesting middle ground
- All others: ON-GRADE default with opt-in skip-grade tracks

## What's NOT in this project (gaps to be aware of)

1. **Disability-type breakdown (Autism specifically)** — NOT on public MI School Data dashboard or CEPI files. Would require formal MI CEPI data request (~weeks turnaround).
2. **Birmingham PS performance data** — curriculum/pathway researched, but no demographic data pulled. Cheapest next-step would be to download equivalent MI CEPI files for Birmingham (6 year folders).
3. **2020-21 (COVID year)** — Troy has partial data (from MI CEPI files); other districts excluded.
4. **WW-P Multilingual Learner sub-categories** — only available in 2024-25; older years lack Current/Former ML breakdown.
5. **NJ 2018-19 demographic coverage** — older SPR format had fewer subgroup rows; race/EL/ECD coverage thinner that year.

## Major decisions worth noting

- **Switched from "SPED-focused" to "G3-G7 Achievement" framing.** Original analysis was SPED-only; user chose to broaden to all demographics for richer analytical lens.
- **Used grade-level aggregation** (n-weighted G3-G7) rather than per-grade for headline comparisons. Per-grade detail still in the data.
- **Excluded Spring 2020** entirely (canceled). Excluded Spring 2021 for most districts (limited admin); kept Troy 2021 from CEPI files where present.
- **Bellevue G3-G5 fix** required field-name correction in OSPI Socrata API config (`organizationleveltestedgrade` → `organizationlevel`). Same fix for all years.

## How to extend this work

1. **Re-run scripts** in `/scripts/` against new data drops (e.g., when 2025-26 testing data publishes).
2. **Add a new district**: replicate one of the per-state extract scripts with the new district's identifiers.
3. **Pull Birmingham PS** — same `MI_TSD_Achievement/` folder structure, just substitute Birmingham's district code (63010) for Troy's (63150) in the CEPI file filter.
4. **Submit MI CEPI data request** if disability-type breakdowns become important — that's the only path to Autism-specific numbers.

Built April 2026.
