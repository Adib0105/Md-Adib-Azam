from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


BASE = Path(__file__).parent
df = pd.read_csv(BASE / "data/students.csv")
df["study_group"] = pd.cut(df["study_hours"], [0, 2, 4, 10], labels=["Up to 2h", "2–4h", "Over 4h"])
group_scores = df.groupby("study_group", observed=False)["exam_score"].mean()
corr = df[["study_hours", "attendance_pct", "assignments_completed", "exam_score"]].corr()["exam_score"]

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
axes[0].scatter(df["study_hours"], df["exam_score"], c=df["attendance_pct"], cmap="viridis", s=65)
axes[0].set_title("Study hours vs exam score")
axes[0].set_xlabel("Study hours per day")
axes[0].set_ylabel("Exam score")
group_scores.plot.bar(ax=axes[1], color="#8b5cf6", title="Average score by study group")
axes[1].set_xlabel("")
axes[1].set_ylabel("Average exam score")
fig.suptitle("Student Performance Analysis", fontsize=16, fontweight="bold")
fig.tight_layout()
(BASE / "outputs").mkdir(exist_ok=True)
fig.savefig(BASE / "outputs/student_performance.png", dpi=160, bbox_inches="tight")
plt.close(fig)

print(f"Average exam score: {df['exam_score'].mean():.1f}")
print(f"Study-hours correlation: {corr['study_hours']:.2f}")
print(f"Attendance correlation: {corr['attendance_pct']:.2f}")
print("Note: correlation describes association and does not prove causation.")
