# 💊 Pharmacovigilance AI Safety Signal System

## AI-Assisted Safety Signal Analysis for Pharmacovigilance Case Data

---

## 📌 1. Project Overview

The Pharmacovigilance AI Safety Signal System is an AI-assisted application designed to analyze pharmacovigilance case data and identify potential safety signals.

The system processes Individual Case Safety Report (ICSR) data and performs structured analysis of:

- Case counts
- Seriousness
- Patient age groups
- Patient sex
- Geographic distribution
- Adverse reactions
- Serious adverse reactions
- Patient outcomes
- Medicinal products
- Drug indications
- Reporting time trends
- Signal-specific evidence

The system then generates a safety signal, calculates a project-specific signal prioritization score, generates an AI-assisted assessment, and produces a final pharmacovigilance report.

---

## 🎯 2. Project Objective

The main objectives of the project are:

1. Load and validate pharmacovigilance case data.
2. Analyze important safety-reporting patterns.
3. Identify frequently reported adverse reactions.
4. Extract evidence related to a selected safety signal.
5. Analyze medicinal products associated with the signal.
6. Calculate a signal prioritization score.
7. Classify the signal priority.
8. Generate an AI-assisted safety assessment.
9. Generate machine-readable JSON and human-readable text reports.
10. Present the results through an interactive Streamlit dashboard.

---

## 🔬 3. Dataset

### Input Dataset

The project uses the following ICSR sample dataset:

`Bisoprolol_icsr_sample_1068rows.xlsx`

### Dataset Statistics

- Total Rows: 1068
- Unique Cases: 1024
- Total Columns: 67

The dataset contains pharmacovigilance case information used for safety signal analysis.

---

## 📊 4. Overall Analysis

The system performs the following analysis steps:

### Case Count Analysis

The system calculates:

- Total number of records
- Number of unique cases

### Seriousness Analysis

The system identifies:

- Serious cases
- Non-serious cases
- Serious case percentage

### Patient Profile Analysis

The system analyzes:

- Age groups
- Sex distribution

### Geographic Analysis

The system analyzes the distribution of reported cases across countries and regions.

### Adverse Reaction Analysis

The system identifies the most frequently reported adverse reactions.

### Serious Reaction Analysis

The system identifies frequently reported serious adverse reactions.

### Outcome Analysis

The system analyzes reported patient outcomes such as:

- Recovered/resolved
- Recovering/resolving
- Fatal
- Not recovered/not resolved/ongoing
- Unknown
- Recovered/resolved with sequelae

### Medicinal Product Analysis

The system identifies frequently reported medicinal products.

### Drug Indication Analysis

The system analyzes the reported indications associated with medicinal products.

### Reporting Time Trend

The system analyzes the number of reports over time.

---

## 🚨 5. Identified Safety Signal

The current analysis identified:

### Acute kidney injury

Signal Cases:

**80**

Signal Rank:

**1**

Signal Score:

**90/100**

Signal Priority:

**HIGH**

Acute kidney injury was the most frequently reported adverse reaction in the analyzed dataset.

---

## 🚨 6. Seriousness Results

The overall dataset contains:

- Serious Cases: 1023
- Not Serious Cases: 1
- Serious Case Percentage: 99.9%

For the selected signal:

- Signal Evidence Cases: 80
- Serious Signal Cases: 80

---

## 👤 7. Patient Profile

### Age Groups

The analyzed dataset contains:

| Age Group   | Cases |
| ----------- | ----: |
| Older Adult |   673 |
| Adult       |   248 |
| Unknown     |    87 |
| Pediatric   |    16 |

### Sex Distribution

| Sex     | Cases |
| ------- | ----: |
| Female  |   503 |
| Male    |   493 |
| Unknown |    28 |

The patient profile analysis helps identify the demographic distribution of reported cases.

---

## 💊 8. Signal-Associated Medicinal Products

Medicinal products reported in cases associated with the selected signal include:

- BISOPROLOL
- FUROSEMIDE
- BISOPROLOL FUMARATE
- ATORVASTATIN
- ASPIRIN
- ALLOPURINOL
- APIXABAN
- AMLODIPINE
- KARDEGIC
- ENTRESTO
- METFORMIN HYDROCHLORIDE
- DAPAGLIFLOZIN
- ACETAMINOPHEN
- RAMIPRIL
- ROSUVASTATIN
- SPIRONOLACTONE
- LEVOTHYROXINE
- PANTOPRAZOLE

The medicinal products are reported in cases associated with the signal.

Co-reporting of a medicinal product with an adverse reaction does not establish causality.

---

## 📈 9. Signal-Specific Outcomes

For the Acute kidney injury signal, the reported outcomes include:

| Outcome                            | Cases |
| ---------------------------------- | ----: |
| Recovered/resolved                 |    39 |
| Recovering/resolving               |    21 |
| Fatal                              |     7 |
| Not recovered/not resolved/ongoing |     6 |
| Unknown                            |     5 |
| Recovered/resolved with sequelae   |     2 |

The signal-specific evidence contains:

**7 fatal outcomes.**

---

## 🌍 10. Signal-Specific Geographic Distribution

The signal-specific cases were reported from multiple countries and regions.

The main reported locations include:

| Country/Region | Signal Cases |
| -------------- | -----------: |
| EU             |           30 |
| France         |           30 |
| United Kingdom |            6 |
| Italy          |            4 |
| Canada         |            3 |
| Spain          |            3 |
| Romania (RO)   |            1 |
| Belgium        |            1 |
| Germany        |            1 |
| Portugal       |            1 |

Geographic distribution is used as supporting reporting-pattern evidence.

---

## 📊 11. Signal Scoring

The project uses a project-specific signal prioritization score.

### Current Signal Score

**90/100**

### Priority

**HIGH**

### Reporting Percentage

**7.81%**

### Fatal Percentage

**8.75%**

### Score Components

The current signal score contains the following components:

| Component         | Score |
| ----------------- | ----: |
| Frequency Score   |    25 |
| Rank Score        |    20 |
| Evidence Score    |    20 |
| Seriousness Score |    15 |
| Fatal Score       |    10 |

### Total

**90/100**

The scoring system is intended for signal prioritization within this project.

It is not a validated causal inference method.

---

## 🤖 12. AI-Assisted Signal Assessment

The system generates an AI-assisted assessment based on the extracted pharmacovigilance evidence.

For the current signal:

Acute kidney injury was the most frequently reported adverse reaction in the analyzed dataset, with 80 reported cases.

The signal-specific evidence contains 80 matching cases.

The signal ranked 1 among the reported adverse reactions.

The signal received a prioritization score of 90/100 and was classified as HIGH priority.

The signal-specific evidence includes 7 fatal outcomes.

The most frequently reported medicinal products associated with the signal include:

- BISOPROLOL
- FUROSEMIDE
- DAPAGLIFLOZIN

These medicinal products were reported in cases associated with the signal.

The observed co-reporting does not establish a causal relationship between a specific medicinal product and the reported reaction.

The findings should therefore be interpreted as reporting-pattern evidence intended to support further pharmacovigilance investigation.

---

## 🧠 13. AI / Analysis Pipeline

The project follows the following processing pipeline:

```text
ICSR Excel Dataset
        ↓
Data Loading
        ↓
Data Validation
        ↓
Case Analysis
        ↓
Seriousness Analysis
        ↓
Patient Profile Analysis
        ↓
Geographic Analysis
        ↓
Adverse Reaction Analysis
        ↓
Medicinal Product Analysis
        ↓
Outcome Analysis
        ↓
Reporting Time Trend
        ↓
Signal Evidence Extraction
        ↓
AI Context Building
        ↓
Safety Signal Generation
        ↓
Signal Scoring
        ↓
AI-Assisted Assessment
        ↓
Report Generation
        ↓
JSON + TXT Reports
        ↓
Streamlit Dashboard
```

📁 14. Project Structure

Gowthami_genar_ai_Challenge/
│
├── data/
│ └── Bisoprolol_icsr_sample_1068rows.xlsx
│
├── prompts/
│
├── reports/
│ ├── acute_kidney_injury_report.json
│ └── acute_kidney_injury_report.txt
│
├── src/
│ ├── ai_generator.py
│ ├── analysis.py
│ ├── dashboard.py
│ ├── data_loader.py
│ ├── evidence.py
│ ├── main.py
│ ├── report_generator.py
│ ├── signal_scoring.py
│ └── validation.py
│
│
├── requirements.txt
│
└── README.md

🧩 15. Source Code Modules

data_loader.py

Responsible for loading the pharmacovigilance dataset.

validation.py

Validates the input dataset and checks required columns.

analysis.py

Performs the main statistical and descriptive analysis.

evidence.py

Extracts evidence related to the selected safety signal.

signal_scoring.py

Calculates the project-specific signal prioritization score.

ai_generator.py

Builds the AI context and generates the AI-assisted safety signal assessment.

report_generator.py

Generates the final text and JSON reports.

main.py

Controls and executes the complete analysis pipeline.

dashboard.py

Provides the interactive Streamlit dashboard for visualization and interpretation.

📊 16. Streamlit Dashboard

The project includes an interactive dashboard with the following sections:

Overview
Signal Evidence
Medicinal Products
Patient Profile
Geography
Signal Scoring
AI Assessment
Limitations

The dashboard provides visual representations of the analyzed pharmacovigilance data.

▶️ 17. How to Run the Project
Step 1: Activate Virtual Environment

On Windows:

venv\Scripts\activate
Step 2: Install Dependencies
pip install -r requirements.txt
Step 3: Run the Analysis Pipeline
python -m src.main
Step 4: Run the Dashboard
python -m streamlit run src/dashboard.py

The Streamlit application will be available at the local URL displayed in the terminal.

📦 18. Requirements

The project requires:

pandas
streamlit
plotly
openpyxl

These dependencies are listed in:

requirements.txt

📄 19. Generated Reports

After running the analysis pipeline, the system generates:

JSON Report
reports/acute_kidney_injury_report.json

The JSON report contains structured analysis results.

Text Report
reports/acute_kidney_injury_report.txt

The text report contains a human-readable summary of the analysis.

⚠️ 20. Limitations

The system has the following limitations:

The analysis is based on reported safety cases.
Reporting frequency does not establish causality.
The signal score is a project-specific prioritization measure.
The signal score is not a validated causal inference method.
Multiple medicinal products may be reported within the same case.
Missing or incomplete patient information may affect subgroup analysis.
The dataset may contain duplicate information across related records.
The system identifies reporting patterns and does not independently confirm clinical causality.
ℹ️ 21. Interpretation

This dashboard presents reporting patterns for pharmacovigilance signal prioritization.

The identified signal should be interpreted as a potential safety signal requiring further investigation.

The signal score is a project-specific prioritization measure.

A HIGH priority classification indicates that the signal has a strong reporting pattern within the analyzed dataset, but it does not prove that a particular medicinal product caused the reported adverse reaction.

Further pharmacovigilance investigation is required to assess the clinical relevance and potential causal relationship.

🔐 22. Safety and Responsible Interpretation

This system is designed as an AI-assisted analytical and prioritization tool.

It should not be used as a standalone clinical decision-making system.

The results should be reviewed by qualified pharmacovigilance professionals before making regulatory or clinical decisions.

🚀 23. Future Scope

Potential future improvements include:

Integration with larger real-world pharmacovigilance datasets
Automated signal detection across multiple adverse reactions
Advanced statistical signal detection methods
Drug-event disproportionality analysis
Natural Language Processing for case narratives
Machine learning-based signal prioritization
Automated duplicate case detection
Advanced temporal trend analysis
Interactive filtering and case-level exploration
Integration with external pharmacovigilance databases
Improved explainability of AI-generated assessments
Automated periodic safety signal monitoring
🎓 24. Project Conclusion

The Pharmacovigilance AI Safety Signal System demonstrates how data analysis, AI-assisted assessment, signal scoring, and interactive visualization can be combined to support pharmacovigilance signal prioritization.

Using the analyzed ICSR sample dataset, the system identified Acute kidney injury as the highest-ranked reported adverse reaction.

The signal was associated with:

80 reported cases
Rank 1
Signal score of 90/100
HIGH priority
7 fatal outcomes

The system provides structured evidence and reporting-pattern analysis to support further pharmacovigilance investigation.

👩‍💻 25. Project Information
Project Title

Pharmacovigilance AI Safety Signal System

Project Type

AI-Assisted Pharmacovigilance Analysis

Main Technologies
Python
Pandas
OpenPyXL
Streamlit
Plotly
JSON
AI-assisted analysis
Input

ICSR pharmacovigilance case dataset

Output
Safety signal analysis
Signal score
AI-assisted assessment
JSON report
Text report
Interactive dashboard
⚖️ Disclaimer

This project is intended for educational, analytical, and research purposes.

The results represent reporting patterns within the analyzed dataset and do not establish causality.

The project-specific signal score should not be interpreted as a validated regulatory or clinical risk score.
