"""
Mini Project: Automated Training Report Generator
==================================================
Demonstrates: Python automation, data aggregation,
              formatted report generation (HTML + optional PDF).

Simulates a tool a training manager would use to auto-generate
weekly learner performance reports — directly relevant to NTUC LearningHub.

Run: python automation_report_generator.py
"""

import os
import random
import datetime
from pathlib import Path

OUTPUT_DIR = Path("report_output")
OUTPUT_DIR.mkdir(exist_ok=True)

# ── Synthetic training data ─────────────────────────────────────────
COURSES = [
    "Fundamentals of Python Programming",
    "Analyse Business Data Using Python",
    "Advanced Analytics & ML Using Python",
    "Deep Learning Models & AI Using Python",
]

def generate_sample_data(n_students: int = 30) -> list:
    random.seed(42)
    names = [
        "Tan Wei Ming","Sarah Lim","Ravi Kumar","Mary Wong","Ahmad Ali",
        "Linda Chen","Kevin Ng","Priya Nair","James Ho","Siti Rahimah",
        "David Lim","Jessica Tan","Muthu K","Rachel Goh","Bryan Ong",
        "Kavitha S","Nurul Ain","Alex Chua","Mei Ling","Raj Patel",
        "Fiona Lim","Eugene Koh","Aisha Malik","Steven Tan","Cheryl Wong",
        "Mohan Das","Grace Yeo","Nicholas Lim","Ramesh Iyer","Joanne Tan",
    ]
    records = []
    for i, name in enumerate(names[:n_students]):
        course = COURSES[i % len(COURSES)]
        quiz   = round(random.uniform(50, 100), 1)
        project= round(random.uniform(55, 100), 1)
        attend = random.randint(75, 100)
        final  = round(quiz * 0.3 + project * 0.5 + attend * 0.2, 1)
        grade  = "Distinction" if final >= 85 else "Merit" if final >= 75 else "Pass" if final >= 60 else "Fail"
        records.append({
            "name"    : name,
            "course"  : course,
            "quiz"    : quiz,
            "project" : project,
            "attendance": attend,
            "final"   : final,
            "grade"   : grade,
        })
    return records


def generate_html_report(records: list) -> str:
    now       = datetime.datetime.now().strftime("%d %B %Y, %H:%M")
    total     = len(records)
    passed    = sum(1 for r in records if r["grade"] != "Fail")
    avg_final = sum(r["final"] for r in records) / total
    top3      = sorted(records, key=lambda r: r["final"], reverse=True)[:3]

    rows_html = ""
    for r in records:
        grade_colour = {
            "Distinction": "#27ae60",
            "Merit"      : "#2980b9",
            "Pass"       : "#f39c12",
            "Fail"       : "#e74c3c",
        }.get(r["grade"], "#555")
        rows_html += f"""
        <tr>
          <td>{r['name']}</td>
          <td>{r['course']}</td>
          <td>{r['quiz']}</td>
          <td>{r['project']}</td>
          <td>{r['attendance']}%</td>
          <td><b>{r['final']}</b></td>
          <td style="color:{grade_colour};font-weight:bold">{r['grade']}</td>
        </tr>"""

    top3_html = "".join(
        f"<li>🏅 <b>{r['name']}</b> — {r['final']} ({r['grade']})</li>"
        for r in top3
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>NTUC LearningHub — Training Performance Report</title>
  <style>
    body {{font-family: 'Segoe UI', sans-serif; margin:40px; color:#2c3e50; background:#f5f6fa;}}
    h1   {{color:#1a252f; border-bottom:3px solid #3498db; padding-bottom:10px;}}
    h2   {{color:#2980b9; margin-top:30px;}}
    .kpi-box {{display:inline-block;background:white;border-radius:8px;
               padding:18px 30px;margin:10px;box-shadow:0 2px 8px rgba(0,0,0,.1);
               text-align:center;min-width:140px;}}
    .kpi-box .val {{font-size:2em;font-weight:bold;color:#2980b9;}}
    .kpi-box .lbl {{font-size:.85em;color:#7f8c8d;margin-top:4px;}}
    table {{border-collapse:collapse;width:100%;background:white;
            border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.08);}}
    th    {{background:#2980b9;color:white;padding:12px 14px;text-align:left;font-size:.9em;}}
    td    {{padding:10px 14px;border-bottom:1px solid #ecf0f1;font-size:.88em;}}
    tr:hover td {{background:#eaf4fb;}}
    ul    {{list-style:none;padding:0;}}
    li    {{padding:6px 0;font-size:.95em;}}
    footer{{margin-top:40px;font-size:.8em;color:#95a5a6;text-align:center;}}
  </style>
</head>
<body>
  <h1>🎓 NTUC LearningHub — Python Training Performance Report</h1>
  <p>Generated: <b>{now}</b></p>

  <h2>📊 Key Performance Indicators</h2>
  <div>
    <div class="kpi-box"><div class="val">{total}</div><div class="lbl">Total Learners</div></div>
    <div class="kpi-box"><div class="val">{passed}</div><div class="lbl">Passed</div></div>
    <div class="kpi-box"><div class="val">{total-passed}</div><div class="lbl">Failed</div></div>
    <div class="kpi-box"><div class="val">{avg_final:.1f}</div><div class="lbl">Avg Final Score</div></div>
    <div class="kpi-box"><div class="val">{passed/total*100:.0f}%</div><div class="lbl">Pass Rate</div></div>
  </div>

  <h2>🏆 Top 3 Learners</h2>
  <ul>{top3_html}</ul>

  <h2>📋 Learner Results</h2>
  <table>
    <thead>
      <tr>
        <th>Name</th><th>Course</th><th>Quiz (30%)</th>
        <th>Project (50%)</th><th>Attendance (20%)</th>
        <th>Final Score</th><th>Grade</th>
      </tr>
    </thead>
    <tbody>{rows_html}</tbody>
  </table>

  <footer>
    Auto-generated by Python Automation Script — NTUC LearningHub Portfolio Demo<br>
    Trainer: [Your Name] | Python Training Domain
  </footer>
</body>
</html>"""
    return html


def main():
    print("\n" + "="*65)
    print("  AUTOMATION MINI PROJECT — TRAINING REPORT GENERATOR")
    print("="*65)

    records  = generate_sample_data()
    html     = generate_html_report(records)
    out_path = OUTPUT_DIR / "training_report.html"

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    total  = len(records)
    passed = sum(1 for r in records if r["grade"] != "Fail")
    print(f"\n  ✓ Report generated: {out_path}")
    print(f"  ✓ Total learners  : {total}")
    print(f"  ✓ Pass rate       : {passed/total*100:.0f}%")
    print(f"  ✓ Avg final score : {sum(r['final'] for r in records)/total:.1f}")
    print("\n  Open training_report.html in any browser to view the formatted report.")
    print("\n  ✅  Automation Report Demo Complete\n")


if __name__ == "__main__":
    main()
