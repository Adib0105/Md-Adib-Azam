from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


BASE = Path(__file__).parent
df = pd.read_csv(BASE / "data/weather.csv")

fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(df["month"], df["avg_high_c"], marker="o", color="#ef4444", label="High °C")
ax1.plot(df["month"], df["avg_low_c"], marker="o", color="#2563eb", label="Low °C")
ax1.set_ylabel("Temperature (°C)")
ax1.set_xlabel("Month")
ax2 = ax1.twinx()
ax2.bar(df["month"], df["rainfall_mm"], alpha=0.25, color="#0ea5e9", label="Rainfall")
ax2.set_ylabel("Rainfall (mm)")
ax1.set_title("Monthly Weather Trends", fontsize=16, fontweight="bold")
lines, labels = ax1.get_legend_handles_labels()
bars, bar_labels = ax2.get_legend_handles_labels()
ax1.legend(lines + bars, labels + bar_labels, loc="upper left")
fig.tight_layout()
(BASE / "outputs").mkdir(exist_ok=True)
fig.savefig(BASE / "outputs/weather_trends.png", dpi=160, bbox_inches="tight")
plt.close(fig)

print(f"Hottest month: {df.loc[df['avg_high_c'].idxmax(), 'month']}")
print(f"Wettest month: {df.loc[df['rainfall_mm'].idxmax(), 'month']}")
print(f"Annual rainfall in sample: {df['rainfall_mm'].sum():,.0f} mm")
print(f"Average yearly high: {df['avg_high_c'].mean():.1f} °C")
