
from pathlib import Path
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter

folder = Path(__file__).resolve().parent

# STEP 1: Load data from our cleaning process
raw = pd.read_csv(folder / "original_sales.csv")
clean = pd.read_csv(folder / "cleaned_sales.csv")
review = pd.read_csv(folder / "needs_review.csv")
duplicates = pd.read_csv(folder / "duplicates.csv")

clean["amount"] = pd.to_numeric(clean["amount"], errors="raise")

# STEP 2: Verify that all original rows are accounted for
assert len(raw) == len(clean) + len(review) + len(duplicates)

# STEP 3: Create a new Excel workbook
wb = Workbook()
summary = wb.active
summary.title = "Summary"

NAVY = "17324D"
TEAL = "087F8C"
PALE = "EAF5F5"
WHITE = "FFFFFF"

# STEP 4: Reusable function for data worksheets
def add_data_sheet(name, df):
    ws = wb.create_sheet(name)
    ws.sheet_view.showGridLines = False

    end_col = len(df.columns)

    ws.merge_cells(
        start_row=1, start_column=1,
        end_row=2, end_column=end_col
    )

    title = ws.cell(1, 1, name)
    title.font = Font(size=17, bold=True, color=WHITE)
    title.fill = PatternFill("solid", fgColor=NAVY)
    title.alignment = Alignment(vertical="center")
    ws.row_dimensions[1].height = 30

    # Column headings
    for col, heading in enumerate(df.columns, start=1):
        cell = ws.cell(4, col, heading)
        cell.font = Font(bold=True, color=WHITE)
        cell.fill = PatternFill("solid", fgColor=TEAL)

    # Data rows
    for row_num, values in enumerate(
        df.itertuples(index=False, name=None), start=5
    ):
        for col_num, value in enumerate(values, start=1):
            if pd.isna(value):
                value = None

            cell = ws.cell(row_num, col_num, value)

            if row_num % 2 == 0:
                cell.fill = PatternFill("solid", fgColor=PALE)

            if df.columns[col_num - 1] == "amount":
                cell.number_format = '#,##0.00'

    # Readability and navigation
    for col, heading in enumerate(df.columns, start=1):
        letter = get_column_letter(col)
        ws.column_dimensions[letter].width = (
            34 if heading == "review_reason" else 23
        )

    ws.freeze_panes = "A5"
    ws.auto_filter.ref = (
        f"A4:{get_column_letter(end_col)}{max(5, 4 + len(df))}"
    )

    return ws


clean_ws = add_data_sheet("Cleaned Sales", clean)
add_data_sheet("Needs Review", review)
add_data_sheet("Duplicates", duplicates)

# STEP 5: Create the dashboard summary
summary.sheet_view.showGridLines = False
summary.merge_cells("A1:H2")
summary["A1"] = "SALES DATA QUALITY REPORT"

for row in summary["A1:H2"]:
    for cell in row:
        cell.fill = PatternFill("solid", fgColor=NAVY)

summary["A1"].font = Font(
    size=20, bold=True, color=WHITE
)
summary["A1"].alignment = Alignment(vertical="center")

summary.column_dimensions["A"].width = 26
summary.column_dimensions["B"].width = 20

metrics = [
    ("Original records", len(raw)),
    ("Valid records",
     f"=COUNTA('Cleaned Sales'!A5:A{max(5, 4 + len(clean))})"),
    ("Needs review",
     f"=COUNTA('Needs Review'!A5:A{max(5, 4 + len(review))})"),
    ("Duplicates",
     f"=COUNTA('Duplicates'!A5:A{max(5, 4 + len(duplicates))})"),
    ("Validated sales (INR)",
     f"=SUM('Cleaned Sales'!C5:C{max(5, 4 + len(clean))})")
]

for row_num, (label, value) in enumerate(metrics, start=5):
    summary.cell(row_num, 1, label)
    result = summary.cell(row_num, 2, value)
    result.font = Font(size=13, bold=True, color=NAVY)

    if row_num == 9:
        result.number_format = '#,##0.00'

summary["A11"] = "Data reconciliation"
summary["B11"] = '=IF(B5=B6+B7+B8,"PASS","REVIEW")'

summary.merge_cells("A13:D15")
summary["A13"] = (
    "Sales totals include only validated transactions. "
    "Review records and duplicates are excluded. "
    "No missing financial values were invented."
)
summary["A13"].alignment = Alignment(
    wrap_text=True, vertical="center"
)
summary["A13"].fill = PatternFill("solid", fgColor=PALE)

# STEP 6: Add a sales-by-customer chart

# STEP 6: Calculate total sales for each customer
customer_totals = (
    clean.groupby("customer", as_index=False)["amount"]
    .sum()
    .sort_values("amount", ascending=False)
)

# Add customer totals to the Summary worksheet
summary["A17"] = "Customer"
summary["B17"] = "Validated Sales (INR)"

for row_num, item in enumerate(
    customer_totals.itertuples(index=False), start=18
):
    summary.cell(row_num, 1, item.customer)
    summary.cell(row_num, 2, float(item.amount))
    summary.cell(row_num, 2).number_format = "#,##0.00"

# Chart the customer totals, not individual transactions

# Insert our professional chart image into Excel
from openpyxl.drawing.image import Image as ExcelImage

chart_path = folder / "sales_chart.png"

if chart_path.exists():
    chart_image = ExcelImage(str(chart_path))
    chart_image.width = 720
    chart_image.height = 400
    summary.add_image(chart_image, "E5")
    print("Inserted sales_chart.png into Excel report")
else:
    print("sales_chart.png not found - chart image not inserted")




      

# STEP 7: Save the finished workbook
output = folder / "Sales_Data_Quality_Report.xlsx"
wb.save(output)

print("Excel report created successfully!")
print("File:", output)
print("Worksheets:", wb.sheetnames)
print("Validated sales:", clean["amount"].sum())
