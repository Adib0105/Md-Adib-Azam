from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


BASE = Path(__file__).parent
df = pd.read_csv(BASE / "data/customers.csv")
df["churn"] = df["churned"].eq("Yes").astype(int)
df["tenure_group"] = pd.cut(df["tenure_months"], [0, 6, 18, 36, 100], labels=["0–6", "7–18", "19–36", "37+"])

by_contract = (df.groupby("contract")["churn"].mean() * 100).sort_values(ascending=False)
by_tenure = df.groupby("tenure_group", observed=False)["churn"].mean() * 100

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
by_contract.sort_values().plot.barh(ax=axes[0], color="#dc2626", title="Churn by contract")
by_tenure.plot.bar(ax=axes[1], color="#7c3aed", title="Churn by tenure")
for ax in axes:
    ax.set_ylabel("Churn rate (%)")
    ax.set_xlabel("")
fig.suptitle("Customer Churn Risk Signals", fontsize=16, fontweight="bold")
fig.tight_layout()
(BASE / "outputs").mkdir(exist_ok=True)
fig.savefig(BASE / "outputs/churn_analysis.png", dpi=160, bbox_inches="tight")
plt.close(fig)

print(f"Overall churn rate: {df['churn'].mean():.1%}")
print(f"Highest-risk contract: {by_contract.index[0]} ({by_contract.iloc[0]:.1f}%)")
print(f"Average tickets — churned: {df.loc[df.churn == 1, 'support_tickets'].mean():.1f}")
print(f"Average tickets — retained: {df.loc[df.churn == 0, 'support_tickets'].mean():.1f}")
