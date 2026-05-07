# MASA Report Full Writing Guide (Draft-Ready)

Use this as a direct writing guide for your preliminary PDF report. Keep body <= 10 pages.

## Page 1 - Executive Summary (What to Write)
Write 3 short subsections:

### 1) Client decision problem
- State who the client is (multinational reinsurer).
- State decision need: quantify climate-risk impact on exposure and identify mitigation priorities.
- State scope: Malaysia vs Vietnam, 2010-2019 history, 2024 projection, 2030 stress scenarios.

Suggested sentence:
> This report evaluates how climate and socio-economic risk drivers influence disaster exposure in Malaysia and Vietnam, and translates those findings into 2030 risk and financial implications for strategic reinsurance planning.

### 2) Key findings (3-4 bullets)
- Country contrast (exposure/adaptive capacity differences).
- Most influential drivers from model.
- 2024 GHG prediction result summary.
- 2030 adverse vs mitigation impact summary.

### 3) Recommended actions (3 bullets)
- Risk-based pricing/underwriting by country profile.
- Mitigation actions tied to highest-impact drivers.
- Protection-gap reduction strategy.

---

## Page 2 - Background, Scope, and Problem Framing

### What to include
- Why climate risk matters for insurers/reinsurers in SEA.
- Why Malaysia and Vietnam are a useful comparative pair.
- Clear problem statement and objectives.
- Explicit out-of-scope statement (e.g., no insurer-level claim microdata).

Suggested structure:
1. Background (1 paragraph)
2. Problem statement (3-4 lines)
3. Objectives (numbered list)
4. Scope and constraints (bullet list)

---

## Page 3 - Data Sources and Preprocessing

### Data source table
For each source include:
- file name
- variable role (feature / target / scenario input)
- time coverage
- known limitations

### Preprocessing narrative
- Country-name harmonization (`Viet Nam` -> `Vietnam`)
- Year filtering logic
- Missing-data handling
- Unit consistency and numeric conversion
- Feature completeness screening

### What judges want here
- Defensible and transparent assumptions
- Reproducible method flow

---

## Page 4 - Preliminary Exploration (EDA)

### Charts to include
- Key climate indicator trends by country
- Disaster events and affected population trend
- Optional disaster-type composition chart

### Interpretation points
- Which country has faster risk-driver growth
- Which country appears more vulnerable/adaptive
- Why this matters for insurance exposure

---

## Page 5 - Feature Engineering and Vulnerability Index

### Write clearly:
- Exposure components used
- Sensitivity components used
- Adaptive-capacity components used
- Formula:
  - `Vulnerability Index = Exposure Score + Sensitivity Score - Adaptive Capacity Score`

### Explain why this index is useful
- Converts multi-dimensional indicators into decision-friendly comparison metric.
- Supports underwriting differentiation.

---

## Page 6 - Required 2024 Climate Indicator Prediction

This page addresses the explicit challenge requirement.

### Include:
- Target indicator: Total GHG emissions including LULUCF (Mt CO2e)
- Modeling approach and split (train <= 2015, test >= 2016 or your actual notebook split)
- Validation metrics (MAE, RMSE, R2)
- 2024 prediction values for each country

### Interpretation
- Is the trend accelerating or stabilizing?
- Which country shows higher projected emissions risk?
- Mention uncertainty and model simplicity.

---

## Page 7 - Disaster Exposure Model and Validation

### Include:
- Target proxy used: `affected_total` (log transformed)
- Model comparison table:
  - trend baseline
  - Ridge
  - Random Forest
- Residual diagnostics figure

### Important explanation
- If Random Forest performs better, state that clearly.
- If Ridge is retained for interpretability, explain tradeoff and governance value.

---

## Page 8 - 2030 Stress Testing

### Write scenario logic
- BAU: trend extrapolation
- Adverse: worsening emissions/ecosystem/vulnerability assumptions
- Mitigation: required adjustments to stabilize or reduce risk

### Add external anchors
- IPCC AR6 high-emission framing
- Insurance-market assumption references

### Show output
- country-level BAU vs adverse vs mitigation comparison
- percentage changes and decision implication

---

## Page 9 - Financial Impact and Recommendations

### Financial translation
- Per-affected cost assumption
- Insured share assumptions by country
- Output:
  - gross expected cost
  - insured portion
  - protection gap
  - mitigation savings vs adverse

### Strategic recommendations (tie each to evidence)
1. Driver-focused mitigation
2. Country-differentiated underwriting
3. Risk-appetite trigger setting from stress results
4. Protection-gap product strategy

---

## Page 10 - Limitations, Uncertainty, and Next Steps

### Limitations to include
- Uneven WDI completeness
- Proxy target vs true claims
- Small sample (2 countries, 10 years)
- Scenario assumption uncertainty

### Next-step roadmap
- Data needed: insurer claim frequency/severity, peril-level exposure
- Modeling upgrade: hierarchical/peril-regional models
- Capital application: reinsurance terms and capital adequacy stress

---

## Bonus-Point Boosters (Add in Report Appendix)
- 2-3 screenshots from `streamlit_app.py` views.
- One paragraph on how decision-makers would use dashboard filters.
- Explicit source links to policy/industry references.
- Clean reproducibility section (commands + outputs).
