
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

folder = Path(__file__).resolve().parent

# Read our validated sales data
df = pd.read_csv(folder / "cleaned_sales.csv")

# Calculate total sales per customer
sales = (
    df.groupby("customer")["amount"]
    .sum()
    .sort_values()
)

# Create a horizontal bar chart
fig, ax = plt.subplots(figsize=(9, 5))

bars = ax.barh(
    sales.index,
    sales.values,
    color="#087F8C"
)

ax.set_title(
    "Validated Sales by Customer",
    fontsize=16,
    fontweight="bold",
    loc="left",
    pad=20
)

ax.set_xlabel("Sales Amount (INR)")
ax.set_xlim(0, sales.max() * 1.25)

# Show amounts next to each bar
ax.bar_label(
    bars,
    labels=[f"₹{v:,.0f}" for v in sales.values],
    padding=6
)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()

# Save as an image
fig.savefig(
    folder / "sales_chart.png",
    dpi=200,
    bbox_inches="tight"
)

plt.close(fig)

print("Professional sales chart created!")
