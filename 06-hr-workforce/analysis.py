from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


BASE = Path(__file__).parent
df = pd.read_csv(BASE / "data/employees.csv")
df["left"] = df["attrition"].eq("Yes").astype(int)
attrition = (df.groupby("department")["left"].mean() * 100).sort_values(ascending=False)
satisfaction = df.groupby("department")["satisfaction"].mean().sort_values(ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
attrition.plot.bar(ax=axes[0], color="#ef4444", title="Attrition rate by department")
satisfaction.plot.bar(ax=axes[1], color="#14b8a6", title="Average satisfaction")
axes[0].set_ylabel("Attrition (%)")
axes[1].set_ylabel("Score (1–5)")
for ax in axes:
    ax.set_xlabel("")
    ax.tick_params(axis="x", rotation=30)
fig.suptitle("HR Workforce Analytics", fontsize=16, fontweight="bold")
fig.tight_layout()
(BASE / "outputs").mkdir(exist_ok=True)
fig.savefig(BASE / "outputs/hr_workforce.png", dpi=160, bbox_inches="tight")
plt.close(fig)

overtime_rates = df.groupby("overtime")["left"].mean() * 100
print(f"Headcount: {len(df)}")
print(f"Overall attrition: {df['left'].mean():.1%}")
print(f"Highest attrition department: {attrition.index[0]} ({attrition.iloc[0]:.1f}%)")
print(f"Attrition with overtime: {overtime_rates.get('Yes', 0):.1f}%")
print(f"Attrition without overtime: {overtime_rates.get('No', 0):.1f}%")
