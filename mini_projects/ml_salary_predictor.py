"""
Mini Project: ML Salary Predictor
==================================
Demonstrates: scikit-learn pipeline, feature encoding,
              cross-validation, model comparison, feature importance.

Run: python ml_salary_predictor.py
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score

OUTPUT_DIR = Path("ml_output")
OUTPUT_DIR.mkdir(exist_ok=True)


def load_clean_data():
    """Load the cleaned data produced by data_analysis.py."""
    try:
        df = pd.read_csv("../project_data_analysis/clean_data.csv")
    except FileNotFoundError:
        print("  ℹ  clean_data.csv not found — run data_analysis.py first.")
        print("  ℹ  Generating synthetic data for demo …\n")
        np.random.seed(42)
        n = 200
        df = pd.DataFrame({
            "Department"      : np.random.choice(["IT","Finance","HR","Data Science","Marketing"], n),
            "Gender"          : np.random.choice(["Male","Female"], n),
            "Education Level" : np.random.choice(["Diploma","Bachelor's","Master's","PhD"], n, p=[0.25,0.35,0.30,0.10]),
            "Seniority Band"  : np.random.choice(["Junior","Mid-Level","Senior","Expert"], n, p=[0.25,0.35,0.25,0.15]),
            "Years Experience": np.random.randint(1, 30, n),
            "Age"             : np.random.randint(22, 58, n),
            "Performance Score": np.random.uniform(2.5, 5.0, n).round(1),
            "Salary"          : None,
        })
        # Synthetic salary with realistic drivers
        edu_mult = {"Diploma":0.8,"Bachelor's":1.0,"Master's":1.2,"PhD":1.5}
        dept_mult = {"IT":1.1,"Finance":1.15,"HR":0.9,"Data Science":1.2,"Marketing":0.95}
        df["Salary"] = (
            3000
            + df["Years Experience"] * 320
            + df["Age"] * 50
            + df["Performance Score"] * 400
            + df["Education Level"].map(edu_mult) * 1500
            + df["Department"].map(dept_mult) * 1000
            + np.random.normal(0, 800, n)
        ).round(0)
    return df


def prepare_features(df: pd.DataFrame):
    """Encode categoricals and build feature matrix."""
    features = ["Department","Gender","Education Level","Seniority Band",
                "Years Experience","Age","Performance Score"]
    df = df[features + ["Salary"]].dropna()

    cat_cols = ["Department","Gender","Education Level","Seniority Band"]
    le = LabelEncoder()
    for col in cat_cols:
        df[col] = le.fit_transform(df[col].astype(str))

    X = df[features].values
    y = df["Salary"].values
    return X, y, features


def compare_models(X_train, X_test, y_train, y_test, feature_names):
    """Train multiple models and compare performance."""
    models = {
        "Linear Regression" : LinearRegression(),
        "Ridge Regression"  : Ridge(alpha=10),
        "Random Forest"     : RandomForestRegressor(n_estimators=100, random_state=42),
        "Gradient Boosting" : GradientBoostingRegressor(n_estimators=100, random_state=42),
    }

    results = []
    best_model = None
    best_r2 = -999

    print(f"\n  {'Model':<25} {'MAE':>10} {'R² Score':>12} {'CV R² Mean':>14}")
    print("  " + "-"*65)

    for name, model in models.items():
        pipe = Pipeline([("scaler", StandardScaler()), ("model", model)])
        pipe.fit(X_train, y_train)
        y_pred = pipe.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        r2  = r2_score(y_test, y_pred)
        cv_scores = cross_val_score(pipe, X_train, y_train, cv=5, scoring="r2")
        print(f"  {name:<25} {mae:>10,.0f} {r2:>12.4f} {cv_scores.mean():>14.4f}")

        results.append({"Model": name, "MAE": mae, "R2": r2, "CV_R2": cv_scores.mean()})
        if r2 > best_r2:
            best_r2 = r2
            best_model = (name, pipe)

    print(f"\n  🏆 Best Model: {best_model[0]}  (R² = {best_r2:.4f})")

    # Feature importance (Random Forest)
    rf_pipe = Pipeline([("scaler", StandardScaler()),
                        ("model", RandomForestRegressor(n_estimators=100, random_state=42))])
    rf_pipe.fit(X_train, y_train)
    importances = rf_pipe.named_steps["model"].feature_importances_
    fi_df = pd.DataFrame({"Feature": feature_names, "Importance": importances})
    fi_df = fi_df.sort_values("Importance", ascending=True)

    # Plot feature importance
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(fi_df["Feature"], fi_df["Importance"],
            color="steelblue", edgecolor="white")
    ax.set_title("Feature Importance — Random Forest Salary Predictor",
                 fontsize=12, fontweight="bold")
    ax.set_xlabel("Importance Score")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "feature_importance.png", dpi=150)
    plt.close()
    print(f"\n  ✓ Feature importance chart saved")

    return pd.DataFrame(results), best_model


def main():
    print("\n" + "="*65)
    print("  ML MINI PROJECT — SALARY PREDICTOR")
    print("="*65)
    df = load_clean_data()
    print(f"  Dataset: {len(df)} records loaded")

    X, y, features = prepare_features(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    print(f"  Train set: {len(X_train)} | Test set: {len(X_test)}")
    results_df, best_model = compare_models(X_train, X_test, y_train, y_test, features)
    print("\n  ✅  Salary Predictor Demo Complete\n")


if __name__ == "__main__":
    main()
