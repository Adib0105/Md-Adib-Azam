from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


BASE = Path(__file__).parent
df = pd.read_csv(BASE / "data/expenses.csv")
df["variance"] = df["actual"] - df["budget"]
by_category = df.groupby("category")[["actual", "budget"]].sum().sort_values("actual", ascending=False)
by_month = df.groupby("month", sort=False)["actual"].sum()

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
by_category.plot.bar(ax=axes[0], color=["#f97316", "#94a3b8"], title="Actual vs budget")
by_month.plot(ax=axes[1], marker="o", linewidth=2.5, color="#2563eb", title="Monthly spending")
axes[0].set_ylabel("Amount (₹)")
axes[0].tick_params(axis="x", rotation=35)
axes[1].set_ylabel("Amount (₹)")
fig.suptitle("Personal Expense Analysis", fontsize=16, fontweight="bold")
fig.tight_layout()
(BASE / "outputs").mkdir(exist_ok=True)
fig.savefig(BASE / "outputs/expense_analysis.png", dpi=160, bbox_inches="tight")
plt.close(fig)

variance = df.groupby("category")["variance"].sum().sort_values(ascending=False)
print(f"Total actual spending: ₹{df['actual'].sum():,.0f}")
print(f"Total budget variance: ₹{df['variance'].sum():+,.0f}")
print(f"Largest overspend category: {variance.index[0]} (₹{variance.iloc[0]:+,.0f})")
