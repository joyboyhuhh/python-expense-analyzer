# Python Expense Analyzer

A small command-line project for exploring fictional expense records with Python and pandas. It validates CSV data, summarizes spending, and saves simple charts as PNG files. It is an educational portfolio project, not a production finance tool.

## Features

- Loads `expenses.csv` and checks for `date`, `category`, `description`, and `amount`.
- Converts dates and amounts to usable types. Rows with invalid or missing values are skipped with a warning; a clear error appears if no valid rows remain.
- Reports total and average spending, transaction count, highest and lowest expenses, highest-spending category, spending by category/date/month, and the five largest transactions.
- Saves a category bar chart and spending-over-time line chart without opening a GUI.

## Technologies

- Python 3
- pandas
- matplotlib
- CSV for the sample data

## Project structure

```text
python-expense-analyzer/
├── .gitignore
├── charts.py
├── expense_analyzer.py
├── expenses.csv
├── README.md
└── requirements.txt
```

Running `charts.py` creates a `charts/` folder with generated PNGs. The folder is excluded from Git because the images can be recreated.

## Setup on Windows PowerShell

From the project folder:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

If PowerShell blocks activation, run the commands using `.venv\Scripts\python.exe` directly, for example:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run the analyzer

```powershell
py expense_analyzer.py
```

## Generate charts

```powershell
py charts.py
```

The command saves `charts/spending_by_category.png` and `charts/spending_over_time.png`. It uses a noninteractive plotting backend, so no chart window is required.

## Example output

The exact formatting may vary slightly by terminal. With the included 18-row dataset, the report includes these summary values:

```text
Transactions:       18
Total spending:     INR 7,330.00
Average expense:    INR 407.22
Highest expense:    INR 910.00 - Fictional grocery shop (2026-10-03)
Lowest expense:     INR 60.00 - Bus fare (2026-09-12)
Highest category:   Food (INR 3,910.00)
```

The report also prints category, date, and monthly totals and lists the five largest expenses.

## Example insights

These values describe only the fictional sample rows in `expenses.csv`:

- Food is the largest category at INR 3,910.
- September totals INR 3,840; October totals INR 3,490 (through October 22 in this sample).
- The largest single row is the fictional grocery shop on October 3 at INR 910.

## What I learned

- Reading CSV data and validating columns and values with pandas.
- Converting text columns to dates and numeric types while handling invalid rows.
- Grouping and aggregating data by category, date, and month.
- Splitting work into small functions and reporting common input errors.
- Creating and saving basic matplotlib charts from analyzed data.

## Future improvements

- Let the user provide a CSV path and currency from the command line.
- Add unit tests for data validation and summary calculations.
- Support filtering reports by a date range.

## Limitations

This beginner-scale example expects a single CSV file with the documented columns. It skips malformed records rather than attempting to repair them. It does not store private account data, connect to banks, or provide budgeting or financial advice.


