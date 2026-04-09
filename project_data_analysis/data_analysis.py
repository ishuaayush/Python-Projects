"""
╔══════════════════════════════════════════════════════════════════════╗
║    Employee Data Analysis & Visualization Pipeline                  ║
║    Author  : Python Trainer Portfolio — NTUC LearningHub            ║
║    Domain  : Data Analytics, AI & Machine Learning                  ║
║    Tools   : pandas, matplotlib, seaborn, scikit-learn, openai API  ║
╚══════════════════════════════════════════════════════════════════════╝

Workflow:
  1. Ingest raw messy CSV data
  2. Clean and transform data (ETL)
  3. Export clean dataset
  4. Perform descriptive analytics
  5. Generate rich data visualizations
  6. (Optional) AI-assisted insights via OpenAI / local LLM

Dependencies:
    pip install pandas numpy matplotlib seaborn scikit-learn openai
"""

import os
import sys
import warnings
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')          # headless rendering — safe for servers / CI
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from datetime import datetime
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────
# Optional AI Integration — Gracefully degrades if key not provided
# ──────────────────────────────────────────────────────────────────────
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

warnings.filterwarnings("ignore")

# ══════════════════════════════════════════════════════════════════════
# 0. CONFIGURATION
# ══════════════════════════════════════════════════════════════════════
RAW_INPUT_FILE   = "raw_data.csv"
CLEAN_OUTPUT_FILE = "clean_data.csv"
OUTPUT_DIR        = Path("output_charts")
OUTPUT_DIR.mkdir(exist_ok=True)

CURRENT_YEAR = datetime.now().year

# ══════════════════════════════════════════════════════════════════════
# 1. DATA INGESTION
# ══════════════════════════════════════════════════════════════════════
def load_raw_data(filepath: str) -> pd.DataFrame:
    """Load raw CSV into a DataFrame and print a preview."""
    print("\n" + "="*65)
    print("  STEP 1 — DATA INGESTION")
    print("="*65)
    df = pd.read_csv(filepath)
    # Strip whitespace from column names (common dirty-data issue)
    df.columns = df.columns.str.strip()
    print(f"  ✓ Loaded {len(df)} rows × {len(df.columns)} columns from '{filepath}'")
    print(f"\n  Column list : {list(df.columns)}")
    print(f"\n  First 3 rows:\n{df.head(3).to_string(index=False)}")
    return df


# ══════════════════════════════════════════════════════════════════════
# 2. DATA QUALITY REPORT (before cleaning)
# ══════════════════════════════════════════════════════════════════════
def data_quality_report(df: pd.DataFrame) -> None:
    """Summarise missing values, duplicates, and type mismatches."""
    print("\n" + "="*65)
    print("  STEP 2 — PRE-CLEANING DATA QUALITY REPORT")
    print("="*65)

    print("\n  ── Missing Values ──")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    quality_df = pd.DataFrame({
        "Missing Count": missing,
        "Missing %"    : missing_pct,
        "Dtype"        : df.dtypes
    })
    print(quality_df[quality_df["Missing Count"] > 0].to_string())

    dup_count = df.duplicated().sum()
    print(f"\n  Duplicate rows  : {dup_count}")
    print(f"  Total records   : {len(df)}")
    print(f"  Total columns   : {len(df.columns)}")

    # Flag obviously incorrect values
    print("\n  ── Potential Data Anomalies ──")
    salary_col = "Salary" if "Salary" in df.columns else None
    if salary_col:
        neg_salary = df[pd.to_numeric(df[salary_col], errors='coerce') < 0]
        print(f"  Negative salaries  : {len(neg_salary)} row(s) — {neg_salary[salary_col].tolist()}")

    age_col = "Age"
    if age_col in df.columns:
        df_age_numeric = pd.to_numeric(df[age_col], errors='coerce')
        unrealistic_age = df[(df_age_numeric > 100) | (df_age_numeric < 18)]
        print(f"  Unrealistic ages   : {len(unrealistic_age)} row(s)")

    unique_gender = df["Gender"].unique() if "Gender" in df.columns else []
    print(f"  Unique Gender values (raw): {list(unique_gender)}")

    unique_status = df["Status"].unique() if "Status" in df.columns else []
    print(f"  Unique Status values (raw): {list(unique_status)}")


# ══════════════════════════════════════════════════════════════════════
# 3. DATA CLEANING & TRANSFORMATION
# ══════════════════════════════════════════════════════════════════════
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Comprehensive cleaning pipeline:
      - Strip whitespace from all string columns
      - Standardise categorical values (Gender, Status)
      - Fix data types (Salary, Age, Performance Score)
      - Parse mixed-format dates
      - Impute or drop missing values
      - Derive new features (Seniority Band, Salary Band, Tenure Years)
      - Remove impossible / erroneous records
    """
    print("\n" + "="*65)
    print("  STEP 3 — DATA CLEANING & TRANSFORMATION")
    print("="*65)

    df = df.copy()

    # ── 3a. Strip whitespace ──────────────────────────────────────────
    str_cols = df.select_dtypes(include="object").columns
    for col in str_cols:
        df[col] = df[col].astype(str).str.strip()
    df.replace({"nan": np.nan, "": np.nan, "None": np.nan}, inplace=True)
    print("  ✓ Stripped leading/trailing whitespace from all string columns")

    # ── 3b. Salary — remove non-numeric chars, convert, drop negatives ─
    df["Salary"] = (
        df["Salary"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace(" ", "", regex=False)
    )
    df["Salary"] = pd.to_numeric(df["Salary"], errors="coerce")
    neg_mask = df["Salary"] < 0
    print(f"  ✓ Salary: converted to numeric. Removed {neg_mask.sum()} negative value(s)")
    df.loc[neg_mask, "Salary"] = np.nan

    # ── 3c. Age — numeric, flag unrealistic values ────────────────────
    df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
    age_mask = (df["Age"] > 100) | (df["Age"] < 16)
    print(f"  ✓ Age: flagged {age_mask.sum()} unrealistic value(s) → set to NaN")
    df.loc[age_mask, "Age"] = np.nan

    # ── 3d. Performance Score — handle 'N/A' strings ──────────────────
    df["Performance Score"] = pd.to_numeric(df["Performance Score"], errors="coerce")
    print("  ✓ Performance Score: converted to numeric")

    # ── 3e. Monthly Bonus — numeric ────────────────────────────────────
    df["Monthly Bonus"] = pd.to_numeric(df["Monthly Bonus"], errors="coerce")

    # ── 3f. Normalise Gender ─────────────────────────────────────────
    gender_map = {
        "Male"  : "Male",   "male"  : "Male",   "M": "Male",
        "Female": "Female", "female": "Female", "F": "Female"
    }
    df["Gender"] = df["Gender"].map(gender_map)
    print("  ✓ Gender: standardised (M/Male/F/Female → Male/Female)")

    # ── 3g. Normalise Status ─────────────────────────────────────────
    df["Status"] = df["Status"].str.title()
    print("  ✓ Status: standardised to Title Case")

    # ── 3h. Standardise Full Name (Title Case) ────────────────────────
    df["Full Name"] = df["Full Name"].str.title()
    df.loc[df["Full Name"].str.strip() == "Nan", "Full Name"] = np.nan
    print("  ✓ Full Name: normalised to Title Case; blanks → NaN")

    # ── 3i. Parse multi-format Join Date ─────────────────────────────
    def try_parse_date(d):
        if pd.isnull(d) or str(d).strip() in ("", "nan"):
            return pd.NaT
        # Handle impossible dates like 30-Feb
        for fmt in ["%d-%b-%Y", "%Y-%m-%d", "%Y/%m/%d",
                    "%m/%d/%Y", "%d/%m/%Y"]:
            try:
                parsed = datetime.strptime(str(d).strip(), fmt)
                # reject Feb 30 etc. — they would have raised ValueError already
                return parsed
            except ValueError:
                continue
        return pd.NaT

    df["Join Date"] = df["Join Date"].apply(try_parse_date)
    invalid_dates = df["Join Date"].isnull().sum()
    print(f"  ✓ Join Date: parsed (multi-format). {invalid_dates} unparseable → NaT")

    # ── 3j. Impute missing numeric values with median ─────────────────
    for col in ["Age", "Salary", "Performance Score", "Monthly Bonus"]:
        n_missing = df[col].isnull().sum()
        if n_missing > 0:
            median_val = df[col].median()
            df[col].fillna(median_val, inplace=True)
            print(f"  ✓ {col}: imputed {n_missing} missing value(s) with median = {median_val:.2f}")

    # ── 3k. Drop rows with no name AND no employee ID ────────────────
    before = len(df)
    df.dropna(subset=["Employee ID"], inplace=True)
    print(f"  ✓ Dropped {before - len(df)} rows with missing Employee ID")

    # ── 3l. Remove duplicate Employee IDs ────────────────────────────
    before = len(df)
    df.drop_duplicates(subset=["Employee ID"], inplace=True)
    print(f"  ✓ Removed {before - len(df)} duplicate Employee ID row(s)")

    # ── 3m. Feature Engineering ───────────────────────────────────────
    # Tenure in years
    df["Tenure Years"] = df["Join Date"].apply(
        lambda d: round((datetime.now() - d).days / 365.25, 1)
        if not pd.isnull(d) else np.nan
    )

    # Seniority Band based on Years Experience
    def seniority(yrs):
        if pd.isnull(yrs):       return "Unknown"
        elif yrs <= 2:           return "Junior"
        elif yrs <= 7:           return "Mid-Level"
        elif yrs <= 15:          return "Senior"
        else:                    return "Expert"

    df["Seniority Band"] = df["Years Experience"].apply(seniority)

    # Salary Band
    def salary_band(sal):
        if pd.isnull(sal):       return "Unknown"
        elif sal < 5000:         return "Entry (<5k)"
        elif sal < 8000:         return "Mid (5k-8k)"
        elif sal < 11000:        return "Senior (8k-11k)"
        else:                    return "Leadership (>11k)"

    df["Salary Band"] = df["Salary"].apply(salary_band)

    # Bonus-to-Salary Ratio
    df["Bonus Ratio %"] = ((df["Monthly Bonus"] / df["Salary"]) * 100).round(2)

    print("\n  ✓ Feature Engineering:")
    print("      → Tenure Years (from Join Date)")
    print("      → Seniority Band (Junior / Mid-Level / Senior / Expert)")
    print("      → Salary Band (Entry / Mid / Senior / Leadership)")
    print("      → Bonus Ratio %")

    # ── 3n. Reset index ───────────────────────────────────────────────
    df.reset_index(drop=True, inplace=True)

    print(f"\n  ✓ Cleaning complete. Final dataset: {len(df)} rows × {len(df.columns)} columns")
    return df


# ══════════════════════════════════════════════════════════════════════
# 4. EXPORT CLEAN DATA
# ══════════════════════════════════════════════════════════════════════
def export_clean_data(df: pd.DataFrame, filepath: str) -> None:
    print("\n" + "="*65)
    print("  STEP 4 — EXPORT CLEAN DATA")
    print("="*65)
    df.to_csv(filepath, index=False, date_format="%Y-%m-%d")
    print(f"  ✓ Clean data saved → '{filepath}'")
    print(f"\n  Clean Dataset Preview (first 5 rows):\n{df.head(5).to_string(index=False)}")


# ══════════════════════════════════════════════════════════════════════
# 5. DESCRIPTIVE ANALYTICS
# ══════════════════════════════════════════════════════════════════════
def descriptive_analytics(df: pd.DataFrame) -> dict:
    """Print and return key statistics summary."""
    print("\n" + "="*65)
    print("  STEP 5 — DESCRIPTIVE ANALYTICS")
    print("="*65)

    stats = {}

    # ── Overall summary ───────────────────────────────────────────────
    print("\n  ── Numeric Summary ──")
    numeric_summary = df[["Age", "Salary", "Performance Score",
                           "Years Experience", "Monthly Bonus",
                           "Tenure Years", "Bonus Ratio %"]].describe().round(2)
    print(numeric_summary.to_string())
    stats["numeric_summary"] = numeric_summary

    # ── Department breakdown ──────────────────────────────────────────
    print("\n  ── Headcount by Department ──")
    dept_count = df["Department"].value_counts()
    print(dept_count.to_string())
    stats["dept_count"] = dept_count

    # ── Average salary by department ─────────────────────────────────
    print("\n  ── Average Salary by Department ──")
    avg_salary_dept = (
        df.groupby("Department")["Salary"]
          .agg(["mean", "median", "min", "max"])
          .round(0)
          .sort_values("mean", ascending=False)
    )
    print(avg_salary_dept.to_string())
    stats["avg_salary_dept"] = avg_salary_dept

    # ── Gender distribution ───────────────────────────────────────────
    print("\n  ── Gender Distribution ──")
    gender_dist = df["Gender"].value_counts()
    print(gender_dist.to_string())
    stats["gender_dist"] = gender_dist

    # ── Top performers ────────────────────────────────────────────────
    print("\n  ── Top 5 Performers (by Performance Score) ──")
    top5 = (
        df[["Full Name", "Department", "Salary", "Performance Score"]]
          .sort_values("Performance Score", ascending=False)
          .head(5)
    )
    print(top5.to_string(index=False))
    stats["top5"] = top5

    # ── Correlation ───────────────────────────────────────────────────
    print("\n  ── Pearson Correlation (key numeric fields) ──")
    corr = df[["Age", "Salary", "Years Experience",
               "Performance Score", "Monthly Bonus"]].corr().round(3)
    print(corr.to_string())
    stats["corr"] = corr

    return stats


# ══════════════════════════════════════════════════════════════════════
# 6. DATA VISUALIZATIONS
# ══════════════════════════════════════════════════════════════════════
def visualize(df: pd.DataFrame, stats: dict) -> None:
    """Create and save all charts to the OUTPUT_DIR."""
    print("\n" + "="*65)
    print("  STEP 6 — DATA VISUALIZATIONS")
    print("="*65)

    palette = "Set2"
    sns.set_theme(style="whitegrid", palette=palette, font_scale=1.05)

    # ── Chart 1: Salary Distribution by Department (Box + Strip) ─────
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(data=df, x="Department", y="Salary", palette=palette,
                showfliers=False, ax=ax, width=0.55)
    sns.stripplot(data=df, x="Department", y="Salary", color="#555555",
                  alpha=0.45, jitter=True, size=5, ax=ax)
    ax.set_title("Salary Distribution by Department", fontsize=15, fontweight="bold", pad=14)
    ax.set_xlabel("Department", fontsize=12)
    ax.set_ylabel("Monthly Salary (SGD)", fontsize=12)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    plt.tight_layout()
    path1 = OUTPUT_DIR / "01_salary_by_department.png"
    plt.savefig(path1, dpi=150)
    plt.close()
    print(f"  ✓ Saved: {path1}")

    # ── Chart 2: Headcount & Avg Salary per Department (Dual-axis) ───
    dept_summary = df.groupby("Department").agg(
        Headcount=("Employee ID", "count"),
        Avg_Salary=("Salary", "mean")
    ).sort_values("Avg_Salary", ascending=False)

    fig, ax1 = plt.subplots(figsize=(11, 6))
    colors = sns.color_palette(palette, len(dept_summary))
    bars = ax1.bar(dept_summary.index, dept_summary["Avg_Salary"],
                   color=colors, width=0.5, label="Avg Salary")
    ax1.set_ylabel("Avg Monthly Salary (SGD)", fontsize=12, color="#2c6e49")
    ax1.tick_params(axis="y", labelcolor="#2c6e49")
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))

    ax2 = ax1.twinx()
    ax2.plot(dept_summary.index, dept_summary["Headcount"],
             color="#d62728", marker="o", linewidth=2.5, markersize=8, label="Headcount")
    ax2.set_ylabel("Headcount", fontsize=12, color="#d62728")
    ax2.tick_params(axis="y", labelcolor="#d62728")

    ax1.set_title("Average Salary vs Headcount by Department",
                  fontsize=14, fontweight="bold", pad=12)
    ax1.set_xlabel("Department", fontsize=12)
    fig.legend(loc="upper right", bbox_to_anchor=(0.92, 0.88), fontsize=11)
    plt.tight_layout()
    path2 = OUTPUT_DIR / "02_dept_salary_headcount.png"
    plt.savefig(path2, dpi=150)
    plt.close()
    print(f"  ✓ Saved: {path2}")

    # ── Chart 3: Performance Score Distribution (KDE + Histogram) ────
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(df["Performance Score"], bins=14, kde=True,
                 color="#4e9af1", edgecolor="white", ax=ax, line_kws={"linewidth": 2.5})
    ax.axvline(df["Performance Score"].mean(), color="#e74c3c",
               linestyle="--", linewidth=2, label=f"Mean = {df['Performance Score'].mean():.2f}")
    ax.axvline(df["Performance Score"].median(), color="#f39c12",
               linestyle=":", linewidth=2, label=f"Median = {df['Performance Score'].median():.2f}")
    ax.set_title("Performance Score Distribution", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Performance Score", fontsize=12)
    ax.set_ylabel("Count", fontsize=12)
    ax.legend(fontsize=11)
    plt.tight_layout()
    path3 = OUTPUT_DIR / "03_performance_distribution.png"
    plt.savefig(path3, dpi=150)
    plt.close()
    print(f"  ✓ Saved: {path3}")

    # ── Chart 4: Correlation Heatmap ──────────────────────────────────
    fig, ax = plt.subplots(figsize=(9, 7))
    corr = stats["corr"]
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f",
                cmap="coolwarm", center=0, linewidths=0.5,
                ax=ax, cbar_kws={"shrink": 0.82})
    ax.set_title("Correlation Heatmap — Key Numeric Variables",
                 fontsize=13, fontweight="bold", pad=12)
    plt.tight_layout()
    path4 = OUTPUT_DIR / "04_correlation_heatmap.png"
    plt.savefig(path4, dpi=150)
    plt.close()
    print(f"  ✓ Saved: {path4}")

    # ── Chart 5: Salary vs Experience (Scatter + Trend) ───────────────
    fig, ax = plt.subplots(figsize=(11, 6))
    scatter_palette = sns.color_palette(palette, df["Department"].nunique())
    dept_colors = {d: scatter_palette[i]
                   for i, d in enumerate(df["Department"].unique())}
    for dept, grp in df.groupby("Department"):
        ax.scatter(grp["Years Experience"], grp["Salary"],
                   label=dept, color=dept_colors[dept],
                   s=70, alpha=0.8, edgecolors="white", linewidths=0.5)
    # Overall trend line
    valid = df[["Years Experience", "Salary"]].dropna()
    z = np.polyfit(valid["Years Experience"], valid["Salary"], 1)
    p = np.poly1d(z)
    x_line = np.linspace(valid["Years Experience"].min(),
                         valid["Years Experience"].max(), 100)
    ax.plot(x_line, p(x_line), "k--", linewidth=2, alpha=0.7, label="Trend")
    ax.set_title("Salary vs Years of Experience (by Department)",
                 fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Years of Experience", fontsize=12)
    ax.set_ylabel("Monthly Salary (SGD)", fontsize=12)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.legend(title="Department", fontsize=9, title_fontsize=10)
    plt.tight_layout()
    path5 = OUTPUT_DIR / "05_salary_vs_experience.png"
    plt.savefig(path5, dpi=150)
    plt.close()
    print(f"  ✓ Saved: {path5}")

    # ── Chart 6: Gender Representation per Department (Stacked Bar) ───
    gender_dept = (
        df.groupby(["Department", "Gender"])
          .size()
          .unstack(fill_value=0)
    )
    fig, ax = plt.subplots(figsize=(11, 6))
    gender_dept.plot(kind="bar", stacked=True, ax=ax,
                     color=["#e07b8c", "#4e9af1"], edgecolor="white", width=0.6)
    ax.set_title("Gender Representation by Department",
                 fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Department", fontsize=12)
    ax.set_ylabel("Headcount", fontsize=12)
    ax.legend(title="Gender", fontsize=11, title_fontsize=11)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=25, ha="right")
    plt.tight_layout()
    path6 = OUTPUT_DIR / "06_gender_by_department.png"
    plt.savefig(path6, dpi=150)
    plt.close()
    print(f"  ✓ Saved: {path6}")

    # ── Chart 7: Seniority Band Distribution (Donut) ──────────────────
    seniority_order = ["Junior", "Mid-Level", "Senior", "Expert"]
    seniority_counts = (
        df["Seniority Band"].value_counts()
          .reindex(seniority_order, fill_value=0)
    )
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        seniority_counts,
        labels=seniority_counts.index,
        autopct="%1.1f%%",
        startangle=140,
        pctdistance=0.78,
        colors=sns.color_palette("Set2", len(seniority_counts)),
        wedgeprops={"edgecolor": "white", "linewidth": 2.5}
    )
    for t in autotexts:
        t.set_fontsize(12)
        t.set_fontweight("bold")
    # Punch out the centre to make it a donut
    centre_circle = plt.Circle((0, 0), 0.55, color="white")
    ax.add_artist(centre_circle)
    ax.set_title("Seniority Band Distribution",
                 fontsize=14, fontweight="bold", pad=16)
    plt.tight_layout()
    path7 = OUTPUT_DIR / "07_seniority_donut.png"
    plt.savefig(path7, dpi=150)
    plt.close()
    print(f"  ✓ Saved: {path7}")

    # ── Chart 8: Avg Performance Score by Education Level ────────────
    edu_order = ["Diploma", "Bachelor's", "Master's", "PhD"]
    edu_perf = (
        df.groupby("Education Level")["Performance Score"]
          .mean()
          .reindex(edu_order)
          .dropna()
          .reset_index()
    )
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(edu_perf["Education Level"], edu_perf["Performance Score"],
                  color=sns.color_palette("coolwarm", len(edu_perf)),
                  edgecolor="white", width=0.5)
    for bar, val in zip(bars, edu_perf["Performance Score"]):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.03,
                f"{val:.2f}", ha="center", va="bottom", fontsize=12, fontweight="bold")
    ax.set_title("Avg Performance Score by Education Level",
                 fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Education Level", fontsize=12)
    ax.set_ylabel("Average Performance Score", fontsize=12)
    ax.set_ylim(0, 6)
    plt.tight_layout()
    path8 = OUTPUT_DIR / "08_performance_by_education.png"
    plt.savefig(path8, dpi=150)
    plt.close()
    print(f"  ✓ Saved: {path8}")

    # ── Chart 9: Dashboard — 4-panel summary ─────────────────────────
    fig = plt.figure(figsize=(18, 12))
    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.40, wspace=0.35)

    # Panel A — Salary by Dept
    ax_a = fig.add_subplot(gs[0, 0])
    dept_avg = df.groupby("Department")["Salary"].mean().sort_values(ascending=True)
    bars = ax_a.barh(dept_avg.index, dept_avg.values,
                     color=sns.color_palette(palette, len(dept_avg)), edgecolor="white")
    for bar, val in zip(bars, dept_avg.values):
        ax_a.text(val + 100, bar.get_y() + bar.get_height()/2,
                  f"${val:,.0f}", va="center", fontsize=9)
    ax_a.set_title("Avg Salary by Department", fontsize=11, fontweight="bold")
    ax_a.set_xlabel("SGD")
    ax_a.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1000:.0f}k"))

    # Panel B — Performance score per dept (violin)
    ax_b = fig.add_subplot(gs[0, 1])
    sns.violinplot(data=df, x="Department", y="Performance Score",
                   palette=palette, ax=ax_b, inner="quartile", cut=0)
    ax_b.set_title("Performance Score — Violin Plot", fontsize=11, fontweight="bold")
    ax_b.set_xlabel("")
    ax_b.set_xticklabels(ax_b.get_xticklabels(), rotation=20, ha="right")

    # Panel C — Salary Band pie
    ax_c = fig.add_subplot(gs[1, 0])
    sb_counts = df["Salary Band"].value_counts()
    ax_c.pie(sb_counts, labels=sb_counts.index, autopct="%1.0f%%",
             startangle=90, colors=sns.color_palette("Set3", len(sb_counts)),
             wedgeprops={"edgecolor": "white"})
    ax_c.set_title("Salary Band Breakdown", fontsize=11, fontweight="bold")

    # Panel D — Tenure vs Performance scatter
    ax_d = fig.add_subplot(gs[1, 1])
    ax_d.scatter(df["Tenure Years"], df["Performance Score"],
                 c=df["Salary"], cmap="YlOrRd", s=70, alpha=0.7, edgecolors="grey", lw=0.3)
    sm = plt.cm.ScalarMappable(cmap="YlOrRd",
                                norm=plt.Normalize(df["Salary"].min(), df["Salary"].max()))
    sm.set_array([])
    fig.colorbar(sm, ax=ax_d, label="Salary (SGD)")
    ax_d.set_title("Tenure vs Performance (colour = Salary)",
                   fontsize=11, fontweight="bold")
    ax_d.set_xlabel("Tenure (Years)")
    ax_d.set_ylabel("Performance Score")

    fig.suptitle("Employee Analytics — Executive Dashboard",
                 fontsize=17, fontweight="bold", y=1.02)
    path9 = OUTPUT_DIR / "09_executive_dashboard.png"
    plt.savefig(path9, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✓ Saved: {path9}")

    print(f"\n  All charts saved in → '{OUTPUT_DIR}/' directory")


# ══════════════════════════════════════════════════════════════════════
# 7. AI-ASSISTED INSIGHTS  (OpenAI GPT-4 / Claude — Optional)
# ══════════════════════════════════════════════════════════════════════
def ai_insights(df: pd.DataFrame, stats: dict) -> None:
    """
    Send a structured summary to an LLM and print AI-generated insights.
    Requires:  OPENAI_API_KEY environment variable
    Model    : gpt-4o  (change to 'gpt-3.5-turbo' for cost savings)
    """
    print("\n" + "="*65)
    print("  STEP 7 — AI-ASSISTED INSIGHTS  (Optional / Bonus)")
    print("="*65)

    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key or not OPENAI_AVAILABLE:
        print("  ℹ  OPENAI_API_KEY not set or openai library not installed.")
        print("     Set the environment variable to enable AI-powered insights.")
        print("     Example:  export OPENAI_API_KEY='sk-...'")
        print("\n  ── Sample AI Prompt (what would be sent) ──")
        sample = build_ai_prompt(df, stats)
        print(sample[:1200] + "\n  [truncated — full prompt sent to model]")
        return

    client = openai.OpenAI(api_key=api_key)
    prompt = build_ai_prompt(df, stats)
    print("  ✓ Sending structured summary to GPT-4o …")
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system",
                 "content": (
                     "You are a senior data analyst. Provide concise, actionable business "
                     "insights from the employee dataset summary provided. Format your "
                     "response with clear sections: Key Findings, Risks, Recommendations."
                 )},
                {"role": "user", "content": prompt}
            ],
            max_tokens=700,
            temperature=0.4
        )
        insight_text = response.choices[0].message.content
        print("\n  ── AI-Generated Insights ──\n")
        print(insight_text)
    except Exception as e:
        print(f"  ✗ OpenAI API error: {e}")


def build_ai_prompt(df: pd.DataFrame, stats: dict) -> str:
    avg_sal = df["Salary"].mean()
    top_dept = stats["avg_salary_dept"]["mean"].idxmax()
    gender_split = stats["gender_dist"].to_dict()
    avg_perf = df["Performance Score"].mean()
    return f"""
Employee Dataset Summary:
- Total Employees    : {len(df)}
- Average Salary     : SGD {avg_sal:,.0f}
- Highest Paid Dept  : {top_dept}
- Gender Split       : {gender_split}
- Average Perf Score : {avg_perf:.2f} / 5.0
- Departments        : {list(df['Department'].unique())}
- Seniority Bands    : {df['Seniority Band'].value_counts().to_dict()}
- Education Levels   : {df['Education Level'].value_counts().to_dict()}
- Top Performers:
{stats['top5'].to_string(index=False)}

Correlation (Salary ~ Years Experience): {df[['Salary','Years Experience']].corr().iloc[0,1]:.3f}

Please provide insights, risks, and recommendations.
"""


# ══════════════════════════════════════════════════════════════════════
# 8. MAIN ENTRYPOINT
# ══════════════════════════════════════════════════════════════════════
def main():
    print("\n" + "█"*65)
    print("  EMPLOYEE DATA ANALYSIS PIPELINE")
    print(f"  Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("█"*65)

    # 1. Load
    df_raw = load_raw_data(RAW_INPUT_FILE)

    # 2. Quality report
    data_quality_report(df_raw)

    # 3. Clean
    df_clean = clean_data(df_raw)

    # 4. Export
    export_clean_data(df_clean, CLEAN_OUTPUT_FILE)

    # 5. Analyse
    stats = descriptive_analytics(df_clean)

    # 6. Visualize
    visualize(df_clean, stats)

    # 7. AI Insights (optional)
    ai_insights(df_clean, stats)

    print("\n" + "█"*65)
    print("  ✅  PIPELINE COMPLETE")
    print(f"  Clean CSV  : {CLEAN_OUTPUT_FILE}")
    print(f"  Charts dir : {OUTPUT_DIR}/")
    print("█"*65 + "\n")


if __name__ == "__main__":
    main()
