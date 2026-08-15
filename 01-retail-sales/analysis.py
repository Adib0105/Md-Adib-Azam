from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


BASE = Path(__file__).parent
df = pd.read_csv(BASE / "data/sales.csv", parse_dates=["date"])
df["revenue"] = df["units"] * df["unit_price"]
df["month"] = df["date"].dt.strftime("%b")

category_sales = df.groupby("category")["revenue"].sum().sort_values(ascending=False)
monthly_sales = df.groupby("month", sort=False)["revenue"].sum()

plt.style.use("seaborn-v0_8-whitegrid")
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
category_sales.sort_values().plot.barh(ax=axes[0], color="#2563eb", title="Revenue by category")
monthly_sales.plot(ax=axes[1], marker="o", linewidth=2.5, color="#f97316", title="Monthly revenue trend")
axes[0].set_xlabel("Revenue (₹)")
axes[0].set_ylabel("")
axes[1].set_ylabel("Revenue (₹)")
axes[1].set_xlabel("")
fig.suptitle("Retail Sales Dashboard", fontsize=16, fontweight="bold")
fig.tight_layout()
(BASE / "outputs").mkdir(exist_ok=True)
fig.savefig(BASE / "outputs/retail_sales_dashboard.png", dpi=160, bbox_inches="tight")
plt.close(fig)

print(f"Total revenue: ₹{df['revenue'].sum():,.0f}")
print(f"Average order value: ₹{df.groupby('order_id')['revenue'].sum().mean():,.0f}")
print(f"Top category: {category_sales.index[0]} (₹{category_sales.iloc[0]:,.0f})")
print(f"Best month: {monthly_sales.idxmax()} (₹{monthly_sales.max():,.0f})")
