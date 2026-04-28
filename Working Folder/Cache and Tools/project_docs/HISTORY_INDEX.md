# History Index — Achievement Project

Reconstructed prompt-by-prompt history of this project, derived from `CONVERSATION_SUMMARY.md` and the artifacts in this folder. Each entry below points to a per-prompt .md with intent, deliverables, and cross-references.

The original chat transcript wasn't included when this project was imported from another computer, so the prompts below are reconstructed from the work that was done — they reflect *what the user clearly asked for*, not the literal text of the original messages.

## Project setup & framing

- [Prompt 01 — Origin question: Troy SPED vs peers](prompt_01_origin_question.md) — the seed question that started everything.
- [Prompt 02 — Peer district selection](prompt_02_peer_selection.md) — Education Recovery Scorecard cohort of 6 peers.
- [Prompt 03 — Add Bellevue WA as an 8th peer](prompt_03_bellevue_added.md) — IM K-12 + scale match.
- [Prompt 04 — Research Birmingham MI as a structural twin](prompt_04_birmingham_research.md) — curriculum match confirmed; data not yet pulled.

## Per-state data extraction

- [Prompt 05 — Pull MI authoritative data for Troy](prompt_05_mi_data_pull.md) — 6 years of CEPI files.
- [Prompt 06 — Pull CAASPP data for the four CA peers](prompt_06_ca_data_pull.md) — Palo Alto, Milpitas, Walnut Valley, Dublin.
- [Prompt 07 — Parse TEA TAPR PDFs for Coppell ISD](prompt_07_tx_tapr_pull.md) — regex on PDFs, no per-grade n.
- [Prompt 08 — Parse NJDOE School Performance Reports + 2024-25 NJSLA bulk Excel](prompt_08_nj_njsla_pull.md) — two formats for WW-P.
- [Prompt 09 — Pull WA OSPI Socrata API for Bellevue](prompt_09_wa_ospi_pull.md) — 5 dataset IDs per year.
- [Prompt 10 — Evaluate SEDA 2024.3 (and rule it out)](prompt_10_seda_ruled_out.md) — no SWD; can't be the spine.

## Pivot, mapping, intermediate artifacts

- [Prompt 11 — Widen the framing from SPED-only to G3-G7 Achievement](prompt_11_widen_to_g3g7.md) — full demographic disaggregation.
- [Prompt 12 — Build the initial SPED comparison spreadsheets](prompt_12_sped_spreadsheets.md) — FY24 + multi-year SWD.
- [Prompt 13 — Combine all per-state CSVs into a master demographics CSV](prompt_13_master_demographics.md) — 5,917 rows.
- [Prompt 14 — Map each district's Math + ELA curriculum](prompt_14_curriculum_mapping.md) — Bridges, Imagine IM, Calkins, district-built.
- [Prompt 15 — Research acceleration pathways per district](prompt_15_acceleration_pathways.md) — on-grade vs compacted-by-default.

## Final deliverables + bug fix + writeup

- [Prompt 16 — Build the interactive dashboard](prompt_16_dashboard_build.md) — single-file `dashboard/index.html`.
- [Prompt 17 — Fix Bellevue G3-G5 OSPI Socrata field-name bug](prompt_17_bellevue_fix.md) — `organizationleveltestedgrade` → `organizationlevel`.
- [Prompt 18 — Build the downloadable XLSX workbook](prompt_18_downloadable_xlsx.md) — 7 sheets, ~229 KB.
- [Prompt 19 — Document the seven key findings](prompt_19_findings_writeup.md) — Bridges, Coppell ELA, Bellevue compaction artifact, etc.
- [Prompt 20 — What's missing and how to extend](prompt_20_gaps_and_extensions.md) — Autism, Birmingham, ML sub-cats, COVID year.

## Related project files (not prompt files)

- [README.md](README.md) — project overview, structure, methodology.
- [CONVERSATION_SUMMARY.md](CONVERSATION_SUMMARY.md) — the source document this index was reconstructed from.
