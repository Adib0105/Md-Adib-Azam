from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


BASE = Path(__file__).parent
df = pd.read_csv(BASE / "data/funnel.csv")
df["step_conversion"] = df["users"].div(df["users"].shift()).mul(100)
df["total_conversion"] = df["users"].div(df["users"].iloc[0]).mul(100)
df["drop_off"] = df["users"].shift() - df["users"]

fig, ax = plt.subplots(figsize=(9, 5))
colors = plt.cm.Blues([0.9, 0.75, 0.6, 0.45, 0.3])
bars = ax.barh(df["stage"][::-1], df["users"][::-1], color=colors)
for bar, value in zip(bars, df["users"][::-1]):
    ax.text(value + 180, bar.get_y() + bar.get_height() / 2, f"{value:,}", va="center")
ax.set_title("E-commerce Conversion Funnel", fontsize=16, fontweight="bold")
ax.set_xlabel("Users")
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
(BASE / "outputs").mkdir(exist_ok=True)
fig.savefig(BASE / "outputs/ecommerce_funnel.png", dpi=160, bbox_inches="tight")
plt.close(fig)

loss_row = df.iloc[1:].loc[df.iloc[1:]["drop_off"].idxmax()]
print(f"Visit-to-purchase conversion: {df['total_conversion'].iloc[-1]:.1f}%")
print(f"Largest drop: before {loss_row['stage']} ({int(loss_row['drop_off']):,} users)")
print(df[["stage", "users", "step_conversion", "total_conversion"]].round(1).to_string(index=False))
