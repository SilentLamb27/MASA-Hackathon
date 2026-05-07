# MASA Hackathon - Climate Risk Assessment (Malaysia vs Vietnam)

This repository contains the full reproducible workflow for preliminary-round submission:
- climate-risk analysis notebook
- supporting data artifacts
- report-generation and validation scripts

## Project Objective
Assess how climate-related drivers can affect disaster exposure and insurance-relevant risk in Malaysia and Vietnam, then translate findings into:
- 2024 climate-indicator projection
- 2030 scenario stress testing
- financial/protection-gap implications
- strategic recommendations

## Repository Structure
- `main_analysis_enhanced.ipynb` - primary analysis notebook for submission
- `streamlit_app.py` - interactive dashboard app for exploratory and appendix visuals
- `REPORT_OUTLINE.md` - 10-page report structure aligned to rubric
- `REPORT_FULL_GUIDE.md` - detailed section-by-section writing guide for the final report draft
- `WB_WDI_WIDEF.csv` - core World Bank WDI wide-format dataset
- `powerbi_fact_climate_indicators.csv` - curated climate indicator panel
- `powerbi_fact_disasters.csv` - disaster-event and affected/deaths panel
- `ghg_2024_prediction.csv` - exported 2024 climate-indicator prediction output
- `generate_final_report.py` - report build helper
- `run_quick_validation.py` - lightweight integrity check
- `requirements.txt` - Python dependencies
- `analysis_summary_for_report.csv`, `limitations_recommendations.csv`, `powerbi_*.csv` - generated report/dashboard artifacts

## Environment Setup
```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

## Reproduce Analysis
1. Open `main_analysis_enhanced.ipynb`.
2. Run all cells from top to bottom.
3. Confirm outputs for:
   - executive summary and rubric checklist
   - WDI feature completeness and vulnerability index
   - required 2024 GHG forecast with validation metrics
   - model comparison and residual diagnostics
   - 2030 BAU/adverse/mitigation stress test
   - financial insured-vs-gap translation
   - robustness and limitations

## Quick Validation
```bash
python run_quick_validation.py
```

## Run Interactive Dashboard (Bonus-Oriented)
```bash
python -m streamlit run streamlit_app.py
```

Dashboard includes:
- climate trend filtering by country/year/indicator
- disaster event and affected comparisons
- 2030 baseline vs stressed damage view
- 2024 GHG prediction view with model-fit metrics
- downloadable filtered CSV outputs

## Report Generation
```bash
python generate_final_report.py
```
Expected output:
- `MASA_Final_Report.pdf`

## Preliminary Submission Checklist
Based on provided criteria:
- Single PDF report in English (`<=10` pages body; formatting-compliant)
- Source code file (`.ipynb`) with clear commented sections
- `README.md` with setup and replication steps
- Optional appendices/supporting files within size/count limits

Recommended submission bundle:
- `MASA_Final_Report.pdf`
- `main_analysis_enhanced.ipynb`
- `REPORT_OUTLINE.md` (optional but recommended during drafting)
- `README.md`
- `requirements.txt`
- `run_quick_validation.py`
- `generate_final_report.py`

## Notes and Assumptions
- `affected_total` is used as a proxy for exposure shock, not insurer-paid claims.
- Scenario stress assumptions should be interpreted as ranges, not deterministic forecasts.
- Insurance-penetration assumptions should be calibrated to current country market reports before final submission.
