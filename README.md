# Sales Data Cleaning & Automated Excel Reporting

A Python-based data cleaning and reporting project that transforms messy sales data into validated, structured Excel reports.

## What This Project Does

- Detects and separates exact duplicate records.
- Identifies missing amounts and invalid dates.
- Standardizes customer names.
- Preserves problematic records for manual review.
- Calculates validated sales and customer-level summaries.
- Generates a formatted Excel workbook with a sales chart.

## Demonstration Results

Tested using 505 fictional sales records.

| Metric | Result |
|---|---|
| Original Records | 505 |
| Valid Transactions | 500 |
| Records Requiring Review | 4 |
| Exact Duplicates | 1 |
| Validated Sales | INR 163,000 |

The validated sales figure includes a controlled ₹500 test adjustment.

## Technologies Used

Python, pandas, openpyxl, matplotlib, CSV and Excel.

## Output

`Sales_Data_Quality_Report.xlsx` contains four worksheets:

1. Summary
2. Cleaned Sales
3. Needs Review
4. Duplicates

## How to Run

Install the dependencies:

```bash
python -m pip install pandas openpyxl matplotlib
```

Run the scripts in this order:

```bash
python clean_data.py
python make_chart.py
python make_excel_report.py
```

The input file should be named `original_sales.csv`.

## Notes

This is an independent portfolio demonstration using fictional business data. It illustrates a defined data-cleaning workflow and has not been represented as paid client work.
