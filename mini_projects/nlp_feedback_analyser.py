"""
Mini Project: NLP Course Feedback Analyser
===========================================
Demonstrates: Text preprocessing, Sentiment Analysis (TextBlob),
              Word frequency, simple visualizations.

Simulates analysing student course feedback — highly relevant
for a training organisation like NTUC LearningHub.

Run: python nlp_feedback_analyser.py
"""

import re
import collections
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

try:
    from textblob import TextBlob
    TEXTBLOB_OK = True
except ImportError:
    TEXTBLOB_OK = False
    print("  ℹ  textblob not installed. Run: pip install textblob")

OUTPUT_DIR = Path("nlp_output")
OUTPUT_DIR.mkdir(exist_ok=True)

# ── Sample course feedback dataset ─────────────────────────────────
FEEDBACK_DATA = [
    {"id": 1, "course": "Python Fundamentals",   "rating": 5, "comment": "Excellent trainer! Very clear explanations and patient with beginners. Loved the hands-on exercises."},
    {"id": 2, "course": "Python Fundamentals",   "rating": 4, "comment": "Good course overall. Content was well structured. Could use more advanced examples at the end."},
    {"id": 3, "course": "ML Using Python",       "rating": 5, "comment": "Amazing! The machine learning section was incredibly insightful. Real-world datasets made it very practical."},
    {"id": 4, "course": "ML Using Python",       "rating": 3, "comment": "Content was okay but the pace was too fast. I struggled to keep up with the ML algorithms section."},
    {"id": 5, "course": "Data Analytics Python", "rating": 5, "comment": "Best Python course I have ever taken. The visualizations chapter was outstanding and very useful for my job."},
    {"id": 6, "course": "Data Analytics Python", "rating": 2, "comment": "Disappointing. The trainer was unprepared and many code examples had errors. Needs improvement."},
    {"id": 7, "course": "Python Fundamentals",   "rating": 4, "comment": "Enjoyable learning experience. Would have liked more time on file handling and exception handling topics."},
    {"id": 8, "course": "ML Using Python",       "rating": 5, "comment": "Very knowledgeable trainer. Deep learning module was fantastic. Already applying skills at work!"},
    {"id": 9, "course": "Data Analytics Python", "rating": 4, "comment": "Informative and well paced. Seaborn and matplotlib labs were very helpful. Good value course."},
    {"id":10, "course": "Python Fundamentals",   "rating": 1, "comment": "Very basic content. Nothing new for someone with prior programming experience. Too slow."},
    {"id":11, "course": "ML Using Python",       "rating": 4, "comment": "Great practical approach. The sklearn pipelines were new to me and extremely valuable."},
    {"id":12, "course": "Data Analytics Python", "rating": 5, "comment": "Trainer was engaging and supportive. Interactive dashboards session was particularly impressive."},
]


def analyse_sentiment(text: str) -> dict:
    """Return polarity, subjectivity, and label using TextBlob."""
    if not TEXTBLOB_OK:
        return {"polarity": 0, "subjectivity": 0, "label": "N/A"}
    blob = TextBlob(text)
    pol = blob.sentiment.polarity
    subj = blob.sentiment.subjectivity
    label = "Positive" if pol > 0.1 else "Negative" if pol < -0.1 else "Neutral"
    return {"polarity": round(pol, 3), "subjectivity": round(subj, 3), "label": label}


def preprocess(text: str) -> list:
    """Lowercase, remove punctuation, tokenise."""
    stopwords = {"the","a","an","and","is","it","to","was","i","for","of",
                 "in","very","with","be","this","that","at","by","my","me",
                 "on","are","had","but","more","have","we","as","so","not","too"}
    tokens = re.findall(r"[a-z]+", text.lower())
    return [t for t in tokens if t not in stopwords and len(t) > 2]


def run_analysis(data: list) -> pd.DataFrame:
    """Enrich feedback records with sentiment scores."""
    rows = []
    for item in data:
        sentiment = analyse_sentiment(item["comment"])
        tokens    = preprocess(item["comment"])
        rows.append({**item, **sentiment, "tokens": tokens})
    return pd.DataFrame(rows)


def visualise(df: pd.DataFrame) -> None:
    import seaborn as sns
    sns.set_theme(style="whitegrid")

    # Sentiment distribution
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # Pie — sentiment label
    counts = df["label"].value_counts()
    colors = {"Positive":"#2ecc71","Neutral":"#f39c12","Negative":"#e74c3c"}
    axes[0].pie(counts, labels=counts.index, autopct="%1.0f%%",
                colors=[colors.get(l,"grey") for l in counts.index],
                startangle=90, wedgeprops={"edgecolor":"white"})
    axes[0].set_title("Overall Sentiment Distribution", fontweight="bold")

    # Bar — avg rating per course
    avg_rating = df.groupby("course")["rating"].mean().sort_values()
    axes[1].barh(avg_rating.index, avg_rating.values,
                 color=sns.color_palette("Set2", len(avg_rating)), edgecolor="white")
    axes[1].set_xlabel("Average Rating (1–5)")
    axes[1].set_title("Average Course Rating", fontweight="bold")
    axes[1].set_xlim(0, 5.5)
    for i, v in enumerate(avg_rating.values):
        axes[1].text(v + 0.05, i, f"{v:.1f}", va="center", fontsize=10)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "sentiment_analysis.png", dpi=150)
    plt.close()
    print(f"  ✓ Saved: {OUTPUT_DIR}/sentiment_analysis.png")

    # Top keywords
    all_tokens = [tok for toks in df["tokens"] for tok in toks]
    top_words = collections.Counter(all_tokens).most_common(15)
    words, freqs = zip(*top_words)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(words, freqs, color=sns.color_palette("husl", len(words)), edgecolor="white")
    ax.set_title("Top 15 Keywords in Course Feedback", fontweight="bold", fontsize=13)
    ax.set_xlabel("Keyword")
    ax.set_ylabel("Frequency")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "top_keywords.png", dpi=150)
    plt.close()
    print(f"  ✓ Saved: {OUTPUT_DIR}/top_keywords.png")


def main():
    print("\n" + "="*65)
    print("  NLP MINI PROJECT — COURSE FEEDBACK ANALYSER")
    print("="*65)
    df = run_analysis(FEEDBACK_DATA)

    print(f"\n  Feedback records analysed: {len(df)}")
    print("\n  ── Sentiment Results ──")
    print(df[["id","course","rating","label","polarity"]].to_string(index=False))

    print(f"\n  Overall avg polarity  : {df['polarity'].mean():.3f}")
    print(f"  Positive feedback     : {(df['label']=='Positive').sum()}")
    print(f"  Negative feedback     : {(df['label']=='Negative').sum()}")

    visualise(df)
    print("\n  ✅  NLP Feedback Analyser Demo Complete\n")


if __name__ == "__main__":
    main()
