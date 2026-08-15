from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


BASE = Path(__file__).parent
df = pd.read_csv(BASE / "data/campaigns.csv")
df["roas"] = df["revenue"] / df["spend"]
df["cac"] = df["spend"] / df["customers"]
df["profit"] = df["revenue"] - df["spend"]
df = df.sort_values("roas", ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
axes[0].bar(df["channel"], df["roas"], color="#16a34a")
axes[0].set_title("Return on ad spend")
axes[0].set_ylabel("ROAS (×)")
axes[0].tick_params(axis="x", rotation=35)
axes[1].bar(df["channel"], df["cac"], color="#0ea5e9")
axes[1].set_title("Customer acquisition cost")
axes[1].set_ylabel("CAC (₹)")
axes[1].tick_params(axis="x", rotation=35)
fig.suptitle("Marketing Channel Performance", fontsize=16, fontweight="bold")
fig.tight_layout()
(BASE / "outputs").mkdir(exist_ok=True)
fig.savefig(BASE / "outputs/marketing_roi.png", dpi=160, bbox_inches="tight")
plt.close(fig)

best = df.iloc[0]
print(f"Best ROAS: {best['channel']} ({best['roas']:.2f}×)")
print(f"Lowest CAC: {df.loc[df['cac'].idxmin(), 'channel']} (₹{df['cac'].min():,.0f})")
print(f"Total campaign profit: ₹{df['profit'].sum():,.0f}")
