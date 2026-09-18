# 🏏 Indian Cricket Coach Selection Prediction Engine

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Dataset: Cricsheet](https://img.shields.io/badge/Dataset-Cricsheet-green.svg)](https://cricsheet.org/)
[![AUC-ROC](https://img.shields.io/badge/Model%20AUC--ROC-0.908-brightgreen.svg)]()

A data-driven machine learning engine that downloads international cricket match data from [Cricsheet](https://cricsheet.org/) spanning **1,021 international matches (2001–2026)** across Tests, ODIs, and T20Is. It maps Indian coaching tenures, extracts detailed cricketer archetypes, and models player selection dynamics to reveal and predict **what kind of cricketers are most likely to play for India under different head coaches**.

---

## 📌 Executive Summary & Key Findings

| Coach | Tenure | Primary Archetype | Total All-Rounders / Match | Left-Hand Batters (LHBs) | Key Distinguishing Feature |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **Gautam Gambhir** | Jul 2024 – Present | Matchup-Driven Multi-Utility All-Rounders & LHB Saturation | 2.11 | **3.92 (All-Time High)** | Extreme LHB bias (Jaiswal, Pant, Dube, Axar, Sundar, Rinku) & highest Left-Arm Pacer odds (1.20) |
| **Rahul Dravid** | Nov 2021 – Jun 2024 | Batting Depth Down to #8/#9 & Attacking Wrist Spin | **2.33 (Highest)** | 3.02 | Dual spin-allrounder pairing (Jadeja + Axar/Sundar) & highest Wrist-Spinner odds (1.33, Kuldeep) |
| **Ravi Shastri** | Jul 2017 – Nov 2021 | The Aggressive 5-Bowler Template & Express Overseas Pace | 1.77 | 2.49 | 4-man express pace battery in SENA Tests (Bumrah, Shami, Ishant, Siraj) & specialist wrist-spin ('Kul-Cha') |
| **Gary Kirsten** | Mar 2008 – Apr 2011 | Specialist Anchors + Part-Time Utility | 1.01 (Lowest) | 2.99 | Top-order anchor preference (1.11 odds); relied on part-timers (Yuvraj, Raina, Sehwag) rather than designated ARs |
| **Duncan Fletcher** | Apr 2011 – Apr 2015 | The Genesis of Modern Spin-Allrounder Template | 1.66 | 3.05 | Transition era: established Ashwin & Jadeja as twin spin all-rounders (1.52 / match) |

---

## 🔬 Modeling Methodology

### 1. Data Pipeline & Zero Lookahead Bias
- **Data Source**: Cricsheet's official `india_male_json.zip` containing 1,021 international matches and 11,245 ball-by-ball individual performance records for 169 Indian players.
- **Contention Pool Construction**: For every match $m$ on date $t$, the candidate pool consists of the 11 selected players ($Y=1$) plus active national contenders who played for India in the previous 18 months ($Y=0$).
- **Strict Rolling Windows**: Player career credentials, 365-day rolling averages, strike rates, economy rates, and wickets per year are computed strictly using data prior to date $t$.

### 2. Statistical & Machine Learning Models
1. **Interaction Logistic Regression Model**:
   - Explicitly estimates interaction terms between Coach dummies and Archetype traits ($\text{Coach} \times \text{PaceAllRounder}$, $\text{Coach} \times \text{WristSpinner}$, $\text{Coach} \times \text{LeftArmPacer}$, etc.).
   - Provides direct, statistically interpretable **odds ratios** ($e^\beta$) for what each coach prioritizes.
   - **Performance**: Train AUC-ROC `0.822`, Accuracy `79.9%`.
2. **5-Fold Cross-Validation Random Forest Ensemble**:
   - Captures non-linear selection rules, recent format activity weights, and venue adjustments.
   - **Performance**: 5-Fold Cross-Validation AUC-ROC `0.9079 +/- 0.0030`.

---

## 📊 Archetype Selection Odds Ratios Across Coaches

*Odds Ratio $> 1.0$ indicates that the coach exhibits a positive preference for that archetype relative to baseline:*

| Archetype Feature | Gary Kirsten | Duncan Fletcher | Ravi Shastri | Rahul Dravid | Gautam Gambhir |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Left-Hand Batter (`is_lhb`)** | **1.51** | 1.24 | 1.06 | 1.15 | 1.14 (Empirical avg: 3.92/11) |
| **Pace All-Rounder (`is_pace_ar`)** | 0.23 | **1.29** | 1.01 | 0.82 | 0.86 |
| **Spin All-Rounder (`is_spin_ar`)** | **1.32** | 1.25 | 0.73 | 0.88 | 0.86 |
| **Specialist Fast Bowler (`is_spec_pace`)** | **1.31** | 1.08 | 1.11 | 1.05 | 0.75 |
| **Specialist Spin Bowler (`is_spec_spin`)**| 1.01 | 0.49 | **1.19** | 0.71 | 1.04 |
| **Left-Arm Pacer (`is_left_arm_pacer`)** | 1.04 | 0.40 | 0.66 | 0.97 | **1.20** |
| **Wrist Spinner (`is_wrist_spinner`)** | 0.77 | 0.62 | 1.07 | **1.33** | 1.06 |
| **Top-Order Anchor (`is_top_order`)** | **1.11** | 1.09 | 0.90 | 0.80 | 0.71 |

---

## 🚀 Quickstart

### 1. Installation
```bash
git clone https://github.com/misrakbc/cricketselection.git
cd cricketselection
pip install -r requirements.txt
```

### 2. Run the Interactive Prediction Tool (CLI)
Evaluate any Indian player across coaches in different formats and conditions:

```bash
# Evaluate Hardik Pandya in T20Is
python predict_selection.py --player "Hardik Pandya" --format "T20I"

# Evaluate Kuldeep Yadav in SENA Tests (Overseas)
python predict_selection.py --player "Kuldeep Yadav" --format "TEST" --sena

# Evaluate Yashasvi Jaiswal in T20Is
python predict_selection.py --player "Yashasvi Jaiswal" --format "T20I"

# Evaluate Axar Patel in ODIs
python predict_selection.py --player "Axar Patel" --format "ODI"
```

### 3. Open the Interactive Web UI
Open `index.html` directly in any web browser to access the graphical dashboard with dynamic dropdowns, format toggles, animated probability bars, and tactical coach breakdowns.

---

## 📁 Repository Structure

```
├── index.html                     # Standalone interactive Web UI / Dashboard
├── data_loader.py                 # Downloads & parses Cricsheet JSON match data
├── feature_builder.py             # Feature engineering & contention pool constructor
├── model_trainer.py               # Logistic Regression interactions & Random Forest trainer
├── player_metadata.py             # Player archetype mappings (roles, hands, styles)
├── predict_selection.py           # Interactive CLI selection prediction engine
├── requirements.txt               # Python package dependencies
├── .gitignore                     # Git ignore rules
└── data/
    └── processed/
        ├── coach_archetype_odds_ratios.csv    # Statistical odds multipliers
        ├── coach_empirical_composition.csv    # Real Playing XI compositions
        ├── feature_importances.csv            # Top selection predictors
        └── interactive_export.json            # Precomputed player-coach scorecards
```

---

## 📜 License
MIT License. Data courtesy of [Cricsheet](https://cricsheet.org/).
