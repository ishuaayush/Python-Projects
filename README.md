```markdown
![Python Portfolio CI](https://github.com/ishuaayush/Python-Projects/actions/workflows/ci.yml/badge.svg)
```

# 🐍 Python Projects Portfolio

---

## 📌 About This Portfolio

This repository demonstrates the breadth and depth of my Python expertise across **four key competency areas** aligned with modern Python curriculum as per industry skill demands:

| # | Area | Skills Showcased |
|---|------|-----------------|
| 1 | **Data Analytics & Visualisation** | pandas, NumPy, matplotlib, seaborn |
| 2 | **Machine Learning & AI** | scikit-learn, TensorFlow/Keras concepts, OpenAI API |
| 3 | **Python Fundamentals & OOP** | Clean code, PEP 8, modular design |
| 4 | **In-Demand Tools (2025)** | Jupyter Notebooks, LLM integration, GitHub CI/CD |

---

## 🗂️ Repository Structure

```
python-portfolio/
│
├── 📁 project_data_analysis/          ← MAIN DEMO PROJECT
│   ├── raw_data.csv                   ← Messy raw employee dataset (input)
│   ├── data_analysis.py               ← Full ETL + analytics + viz pipeline
│   ├── clean_data.csv                 ← Generated clean output
│   └── output_charts/                 ← Generated PNG visualizations
│       ├── 01_salary_by_department.png
│       ├── 02_dept_salary_headcount.png
│       ├── 03_performance_distribution.png
│       ├── 04_correlation_heatmap.png
│       ├── 05_salary_vs_experience.png
│       ├── 06_gender_by_department.png
│       ├── 07_seniority_donut.png
│       ├── 08_performance_by_education.png
│       └── 09_executive_dashboard.png
│
├── 📁 notebooks/                      ← Jupyter Notebooks
│   └── 01_data_analysis_walkthrough.ipynb
│
├── 📁 mini_projects/                  ← Bite-sized demos per skill area
│   ├── ml_salary_predictor.py         ← ML: Salary prediction (scikit-learn)
│   ├── nlp_feedback_analyser.py       ← NLP: Sentiment on course feedback
│   ├── chatbot_ai_assistant.py        ← GenAI: OpenAI-powered Q&A bot
│   └── automation_report_generator.py ← Automation: PDF report builder
│
├── requirements.txt
├── .gitignore
└── README.md                          ← (this file)
```

---

## 🚀 Main Project — Employee Data Analysis Pipeline

### Problem Statement
Real-world HR datasets are messy: inconsistent date formats, negative salaries, missing names, mixed gender encodings, unrealistic ages, and more. This project simulates a real ETL + analytics scenario.

### Pipeline Overview

```
raw_data.csv
     │
     ▼
[1] Data Ingestion       → Load CSV, inspect shape & dtypes
     │
     ▼
[2] Quality Report       → Missing values, duplicates, anomalies
     │
     ▼
[3] Data Cleaning        → Standardise, impute, validate, engineer features
     │
     ▼
[4] Export Clean CSV     → clean_data.csv
     │
     ▼
[5] Descriptive Analytics → Stats, group-by, correlation
     │
     ▼
[6] Visualizations       → 9 publication-ready charts
     │
     ▼
[7] AI Insights          → Optional GPT-4o narrative summary
```

### Data Issues Handled (Dirty → Clean)

| Issue | Example | Fix Applied |
|-------|---------|-------------|
| Mixed date formats | `15-Jan-2020`, `2021/03/22`, `01/07/2018` | Multi-format parser |
| Impossible date | `30-Feb-2021` | Caught → `NaT` |
| Negative salary | `-7500` | Set to `NaN`, imputed with median |
| Unrealistic age | `200` | Flagged & removed |
| Inconsistent gender | `M`, `F`, `Male`, `Female` | Normalised map |
| Mixed case status | `active`, `ACTIVE`, `Active` | `.str.title()` |
| Trailing whitespace | `"Salary "` (column name) | `.str.strip()` |
| Missing numeric values | Blank Salary, Bonus | Median imputation |
| Non-numeric 'N/A' | `"N/A"` in Performance Score | `pd.to_numeric(errors='coerce')` |

### Feature Engineering

| New Feature | Logic |
|-------------|-------|
| `Tenure Years` | Days since Join Date ÷ 365.25 |
| `Seniority Band` | Junior / Mid-Level / Senior / Expert (based on experience) |
| `Salary Band` | Entry / Mid / Senior / Leadership (based on salary) |
| `Bonus Ratio %` | Monthly Bonus ÷ Salary × 100 |

---

## 📊 Visualizations Generated

| Chart | Type | Insight |
|-------|------|---------|
| Salary Distribution by Dept | Box + Strip Plot | Spread and outliers per department |
| Avg Salary vs Headcount | Dual-Axis Bar + Line | Resource allocation overview |
| Performance Score Distribution | Histogram + KDE | Talent curve shape |
| Correlation Heatmap | Seaborn Heatmap | Relationships between numeric fields |
| Salary vs Experience (Dept) | Scatter + Trend Line | Experience-pay progression |
| Gender Representation | Stacked Bar | Diversity view per department |
| Seniority Band | Donut Pie | Workforce composition |
| Perf Score by Education | Bar Chart | Education-performance link |
| Executive Dashboard | 4-Panel Grid | One-page management summary |

---

## 🤖 AI & In-Demand Tools Integration

### Tools & Technologies Demonstrated

| Tool / Library | Use Case | Industry Relevance |
|---------------|----------|--------------------|
| **pandas** | Data wrangling & ETL | Core data engineering skill |
| **NumPy** | Numerical computation | Foundation of all ML libraries |
| **matplotlib + seaborn** | Visualisation | Standard in data analytics roles |
| **scikit-learn** | ML models (salary predictor) | Most widely used ML library |
| **OpenAI API (GPT-4o)** | AI-driven narrative insights | Generative AI integration trend |
| **Jupyter Notebook** | Interactive exploration | Industry standard for data science |
| **GitHub Actions** | CI/CD pipeline | DevOps for data projects |
| **python-docx / reportlab** | Automated PDF/Word reports | Business automation |
| **NLTK / TextBlob** | Sentiment analysis | NLP for feedback analytics |

### 🧠 Generative AI Integration
The pipeline includes an optional **Step 7** that connects to **OpenAI's GPT-4o** to generate plain-English business insights from the analytics summary. This demonstrates:
- LLM API integration in Python
- Prompt engineering best practices
- Graceful degradation (works without API key)

---

## ⚙️ Setup & Run

### Prerequisites
```bash
Python 3.9+
pip
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Main Project
```bash
cd project_data_analysis
python data_analysis.py
```

**Outputs generated:**
- `clean_data.csv` — cleaned employee dataset
- `output_charts/*.png` — 9 visualisation charts

### Enable AI Insights (Optional)
```bash
export OPENAI_API_KEY="sk-your-api-key-here"
python data_analysis.py
```

### Run in Jupyter Notebook
```bash
jupyter notebook notebooks/01_data_analysis_walkthrough.ipynb
```

---

## 🎓 Alignment with Curriculum

This portfolio directly supports the following Python courses:

| Course | Skills Covered in This Portfolio |
|-------------|----------------------------------|
| **Fundamentals of Python Programming** | OOP, file I/O, control flow, functions |
| **Analyse Business Data Using Python** | pandas, matplotlib, dashboards |
| **Advanced Analytics & ML Using Python** | scikit-learn, feature engineering, model evaluation |
| **Deep Learning Models & AI Using Python** | Neural network concepts, TensorFlow/Keras patterns |
| **Generative AI for Business Professionals** | OpenAI API, prompt engineering, LLM integration |

---

## 👤 About the Trainer

I am a Python practitioner with hands-on experience across data analytics, machine learning, and AI integration. As a trainer, I believe in:

- **Learning by doing** — every concept tied to a real-world dataset
- **Progressive complexity** — from syntax basics to production pipelines
- **Industry relevance** — tools and workflows used by Singapore employers today
- **Inclusive teaching** — PMETs, fresh graduates, and career switchers equally welcome

---

