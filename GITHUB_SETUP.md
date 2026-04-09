# 🚀 GitHub Repository Setup Guide
### NTUC LearningHub — Python Trainer Portfolio

---

## Overview

This guide walks you through every step to publish your portfolio as a professional GitHub repository — from creating your account to adding a CI/CD badge to your README.

---

## PART 1 — Prerequisites

### 1.1 Install Git (if not already installed)

**Windows:**
```
https://git-scm.com/download/win
```
Download and run the installer. Accept all defaults.

**macOS:**
```bash
brew install git        # if you have Homebrew
# OR install Xcode Command Line Tools:
xcode-select --install
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update && sudo apt install git
```

**Verify installation:**
```bash
git --version
# Expected output: git version 2.x.x
```

---

### 1.2 Configure Git Identity

Run these once on your machine (replace with your details):
```bash
git config --global user.name  "Your Full Name"
git config --global user.email "your.email@example.com"
```

---

## PART 2 — Create Your GitHub Account & Repository

### 2.1 Create GitHub Account
1. Go to **https://github.com**
2. Click **Sign up**
3. Choose a professional username — e.g. `yourname-dev` or `johntanpython`
4. Verify your email address

### 2.2 Create the Repository
1. Click the **+** icon (top-right) → **New repository**
2. Fill in:
   - **Repository name:** `ntuc-python-portfolio`
   - **Description:** `Python Trainer Portfolio — NTUC LearningHub | Data Analytics, ML & AI`
   - **Visibility:** ✅ Public  *(required for recruiters/interviewers to view)*
   - **Add a README:** ❌ Leave unchecked *(we have our own)*
   - **Add .gitignore:** ❌ Leave unchecked *(we have our own)*
3. Click **Create repository**

You will land on an empty repo page — copy the URL shown, e.g.:
```
https://github.com/YOUR_USERNAME/ntuc-python-portfolio.git
```

---

## PART 3 — Push the Portfolio to GitHub

Open your terminal and run the following commands **from inside the portfolio folder**:

```bash
# Step 1 — Navigate to your portfolio directory
cd /path/to/ntuc-python-portfolio

# Step 2 — Initialise git
git init

# Step 3 — Stage all files
git add .

# Step 4 — First commit
git commit -m "Initial commit — NTUC LearningHub Python Trainer Portfolio"

# Step 5 — Set the branch name to main
git branch -M main

# Step 6 — Link to your GitHub repository (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/ntuc-python-portfolio.git

# Step 7 — Push to GitHub
git push -u origin main
```

**If prompted for credentials:**
- Username: your GitHub username
- Password: use a **Personal Access Token** (see Part 4)

---

## PART 4 — Personal Access Token (GitHub Authentication)

GitHub no longer accepts plain passwords. You need a token.

### 4.1 Generate a Token
1. GitHub → click your **profile picture** → **Settings**
2. Left sidebar → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
3. Click **Generate new token (classic)**
4. Set:
   - Note: `portfolio-push`
   - Expiration: `90 days` (or No expiration)
   - Scopes: ✅ **repo** (full control)
5. Click **Generate token**
6. **Copy the token immediately** — GitHub only shows it once

Use this token as your password when `git push` prompts for it.

### 4.2 Optional: Save Credentials (so you don't retype each time)
```bash
git config --global credential.helper store
```
After your first authenticated push, credentials are saved locally.

---

## PART 5 — Verify the Repository

1. Open your browser: `https://github.com/YOUR_USERNAME/ntuc-python-portfolio`
2. You should see:
   - Your full `README.md` rendered with tables and formatting
   - All folders: `project_data_analysis/`, `mini_projects/`, `.github/`
   - All `.ipynb` notebooks listed
   - The `.py` scripts and CSV files

---

## PART 6 — GitHub Actions (Automated CI/CD)

The `.github/workflows/ci.yml` file is already included in the portfolio. Once you push, GitHub automatically:

1. Spins up an Ubuntu environment
2. Installs all Python dependencies
3. Runs `data_analysis.py` end-to-end
4. Verifies `clean_data.csv` and all 9 charts were generated
5. Uploads the charts as downloadable build artifacts

### 6.1 View the CI Workflow
- Go to your repo → click **Actions** tab
- You should see `Python Portfolio CI` running (or completed ✅)

### 6.2 Add a CI Badge to README

Copy this line and add it near the top of your `README.md`:
```markdown
![Python Portfolio CI](https://github.com/YOUR_USERNAME/ntuc-python-portfolio/actions/workflows/ci.yml/badge.svg)
```
Replace `YOUR_USERNAME` with your actual GitHub username.

The badge shows live status — green tick = pipeline passing ✅

---

## PART 7 — Making the Repo Interview-Ready

### 7.1 Pin the Repository to Your Profile
1. Go to `https://github.com/YOUR_USERNAME`
2. Click **Customize your pins**
3. Select `ntuc-python-portfolio` → **Save pins**

The repo will now appear prominently on your profile page.

### 7.2 Add Repository Topics
On the repo page → click the ⚙️ gear next to **About** → add topics:
```
python  data-analytics  machine-learning  pandas  matplotlib
seaborn  scikit-learn  openai  jupyter  ntuc  data-science
```

### 7.3 Add a Short Description
In the same **About** panel:
```
Python Trainer Portfolio for NTUC LearningHub — Data Analytics, ML & AI | pandas · scikit-learn · OpenAI API
```

### 7.4 Upload Sample Chart (Repository Social Preview)
1. Settings → **Social preview**
2. Upload `output_charts/09_executive_dashboard.png`
This becomes the preview image when you share the link on LinkedIn.

---

## PART 8 — Keeping Your Portfolio Updated

### After any changes:
```bash
git add .
git commit -m "Update: describe what you changed"
git push
```

### Common commands:
```bash
git status          # see what's changed
git log --oneline   # see commit history
git diff            # see line-level changes
```

---

## PART 9 — LinkedIn & Interview Tips

### Share on LinkedIn
Post your GitHub link with this caption:
> "Just published my Python Data Analytics portfolio — built for my NTUC LearningHub Trainer interview!
> Covers ETL pipelines, 9 visualizations, scikit-learn ML models, NLP sentiment analysis,
> and OpenAI GPT-4o integration. Built with pandas, seaborn, matplotlib, and Jupyter.
> 🔗 [your GitHub link]
> #Python #DataAnalytics #MachineLearning #NTUCLearningHub #SkillsFuture"

### In the Interview — Talking Points
When demo-ing `01_Employee_Data_Analysis_Pipeline.ipynb`:

1. **"Here is the raw data"** — open `raw_data.csv`, point out the intentional issues
2. **"Here is what the quality report finds"** — run Cell 3 to show the anomaly summary
3. **"Here is the cleaning step by step"** — walk through Cell 4, explain each fix
4. **"Here is the clean output"** — show `clean_data.csv` side by side
5. **"Here are the visualisations"** — run cells 5–13, explain each chart choice
6. **"Here is the AI integration"** — show Cell 14, explain prompt engineering

---

## PART 10 — Folder Structure Reference

```
ntuc-python-portfolio/
│
├── .github/
│   └── workflows/
│       └── ci.yml                     ← CI/CD pipeline
│
├── project_data_analysis/
│   ├── raw_data.csv                   ← Messy 40-row HR dataset
│   ├── data_analysis.py               ← Python script version
│   ├── 01_Employee_Data_Analysis_Pipeline.ipynb  ← Jupyter notebook
│   ├── clean_data.csv                 ← Generated clean output
│   └── output_charts/
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
├── mini_projects/
│   ├── ml_salary_predictor.py
│   ├── 02_ML_Salary_Predictor.ipynb
│   ├── nlp_feedback_analyser.py
│   ├── 03_NLP_Feedback_Analyser.ipynb
│   ├── chatbot_ai_assistant.py
│   ├── 04_AI_Chatbot_Assistant.ipynb
│   ├── automation_report_generator.py
│   └── 05_Automation_Report_Generator.ipynb
│
├── README.md
├── requirements.txt
├── .gitignore
└── GITHUB_SETUP.md                    ← This file
```

---

*Guide prepared for NTUC LearningHub Python Trainer Interview*
*Last updated: April 2026*
