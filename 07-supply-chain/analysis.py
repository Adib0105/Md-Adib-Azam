from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


BASE = Path(__file__).parent
df = pd.read_csv(BASE / "data/shipments.csv")
df["delay_days"] = df["actual_days"] - df["promised_days"]
df["on_time"] = df["delay_days"].le(0).astype(int)
carrier_rate = (df.groupby("carrier")["on_time"].mean() * 100).sort_values(ascending=False)
region_delay = df.groupby("region")["delay_days"].mean().sort_values(ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
carrier_rate.plot.bar(ax=axes[0], color="#22c55e", title="On-time rate by carrier")
region_delay.plot.bar(ax=axes[1], color="#f59e0b", title="Average delay by region")
axes[0].set_ylabel("On-time deliveries (%)")
axes[1].set_ylabel("Delay (days)")
for ax in axes:
    ax.set_xlabel("")
    ax.tick_params(axis="x", rotation=25)
fig.suptitle("Supply Chain Delivery Performance", fontsize=16, fontweight="bold")
fig.tight_layout()
(BASE / "outputs").mkdir(exist_ok=True)
fig.savefig(BASE / "outputs/supply_chain.png", dpi=160, bbox_inches="tight")
plt.close(fig)

print(f"Overall on-time rate: {df['on_time'].mean():.1%}")
print(f"Best carrier: {carrier_rate.index[0]} ({carrier_rate.iloc[0]:.1f}%)")
print(f"Region with highest average delay: {region_delay.index[0]} ({region_delay.iloc[0]:.2f} days)")
print(f"Average shipping cost: ₹{df['shipping_cost'].mean():,.0f}")
