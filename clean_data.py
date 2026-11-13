
from pathlib import Path
import pandas as pd

folder = Path(__file__).resolve().parent

# 1. Read the original data without changing it
raw = pd.read_csv(
    folder / "original_sales.csv",
    dtype=str,
    keep_default_na=False
)

# 2. Separate exact duplicate rows
duplicate_mask = raw.duplicated()
duplicates = raw.loc[duplicate_mask].copy()
data = raw.loc[~duplicate_mask].copy()

# 3. Standardize names and IDs
data["order_id"] = data["order_id"].str.strip()
data["customer"] = data["customer"].str.strip().str.title()

# 4. Check amounts and dates
amounts = pd.to_numeric(
    data["amount"].str.strip(), errors="coerce"
)

dates = pd.to_datetime(
    data["order_date"].str.strip(),
    format="%Y-%m-%d",
    errors="coerce"
)

# 5. Define what makes a valid transaction
valid_mask = (
    data["order_id"].ne("")
    & data["customer"].ne("")
    & amounts.notna()
    & amounts.ge(0)
    & dates.notna()
)

# 6. Keep valid records
cleaned = data.loc[valid_mask].copy()
cleaned["amount"] = amounts.loc[valid_mask]
cleaned["order_date"] = dates.loc[valid_mask].dt.strftime(
    "%Y-%m-%d"
)

# 7. Preserve problematic records for review
review = data.loc[~valid_mask].copy()

def explain_issue(index):
    reasons = []
    if not data.at[index, "order_id"]:
        reasons.append("Missing order ID")
    if not data.at[index, "customer"]:
        reasons.append("Missing customer")
    if pd.isna(amounts.at[index]) or amounts.at[index] < 0:
        reasons.append("Missing or invalid amount")
    if pd.isna(dates.at[index]):
        reasons.append("Invalid date")
    return "; ".join(reasons)

review["review_reason"] = [
    explain_issue(i) for i in review.index
]

# 8. Export the results
cleaned.to_csv(folder / "cleaned_sales.csv", index=False)
review.to_csv(folder / "needs_review.csv", index=False)
duplicates.to_csv(folder / "duplicates.csv", index=False)

# 9. Verify that no records disappeared
assert len(raw) == len(cleaned) + len(review) + len(duplicates)

print("Original records:", len(raw))
print("Valid records:", len(cleaned))
print("Records needing review:", len(review))
print("Duplicates:", len(duplicates))
print("Validated sales total:", cleaned["amount"].sum())

print("\nRecords needing review:")
print(review.to_string(index=False))
