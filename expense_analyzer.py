"""Analyze fictional expense records stored in expenses.csv."""

from pathlib import Path
import pandas as pd

CSV_PATH = Path(__file__).with_name("expenses.csv")
REQUIRED_COLUMNS = {"date", "category", "description", "amount"}


def load_expenses(csv_path=CSV_PATH):
    """Read and validate expenses, skipping rows with invalid fields."""
    try:
        expenses = pd.read_csv(csv_path)
    except FileNotFoundError as exc:
        raise ValueError(f"CSV file was not found: {csv_path}") from exc
    except pd.errors.EmptyDataError as exc:
        raise ValueError(f"CSV file is empty: {csv_path}") from exc
    except (OSError, pd.errors.ParserError) as exc:
        raise ValueError(f"Could not read CSV file '{csv_path}': {exc}") from exc

    missing_columns = REQUIRED_COLUMNS - set(expenses.columns)
    if missing_columns:
        raise ValueError(f"CSV is missing required column(s): {', '.join(sorted(missing_columns))}")
    if expenses.empty:
        raise ValueError("CSV contains a header but no expense rows.")

    expenses = expenses.copy()
    expenses["date"] = pd.to_datetime(expenses["date"], errors="coerce")
    expenses["amount"] = pd.to_numeric(expenses["amount"], errors="coerce")
    expenses["category"] = expenses["category"].astype("string").str.strip()
    expenses["description"] = expenses["description"].astype("string").str.strip()
    valid = (expenses["date"].notna() & expenses["amount"].notna()
             & expenses["category"].notna() & expenses["category"].ne("")
             & expenses["description"].notna() & expenses["description"].ne(""))
    skipped = int((~valid).sum())
    expenses = expenses.loc[valid].copy()
    if skipped:
        print(f"Warning: skipped {skipped} row(s) with invalid or missing values.")
    if expenses.empty:
        raise ValueError("No valid expense rows remain after checking dates, amounts, category, and description.")
    return expenses.sort_values("date")


def calculate_summary(expenses):
    """Return totals and grouped views for valid expense rows."""
    return {
        "total": expenses["amount"].sum(),
        "average": expenses["amount"].mean(),
        "highest": expenses.loc[expenses["amount"].idxmax()],
        "lowest": expenses.loc[expenses["amount"].idxmin()],
        "count": len(expenses),
        "categories": expenses.groupby("category")["amount"].sum().sort_values(ascending=False),
        "dates": expenses.groupby("date")["amount"].sum().sort_index(),
        "monthly": expenses.groupby(expenses["date"].dt.to_period("M"))["amount"].sum().sort_index(),
        "top_five": expenses.nlargest(5, "amount"),
    }


def print_summary(summary):
    """Print a readable report in the terminal."""
    print("\nExpense Analyzer Summary\n" + "=" * 42)
    print(f"Transactions:       {summary['count']}")
    print(f"Total spending:     INR {summary['total']:,.2f}")
    print(f"Average expense:    INR {summary['average']:,.2f}")
    high, low = summary["highest"], summary["lowest"]
    print(f"Highest expense:    INR {high['amount']:,.2f} - {high['description']} ({high['date'].date()})")
    print(f"Lowest expense:     INR {low['amount']:,.2f} - {low['description']} ({low['date'].date()})")
    categories = summary["categories"]
    print(f"Highest category:   {categories.index[0]} (INR {categories.iloc[0]:,.2f})")
    print("\nSpending by category:")
    for category, amount in categories.items():
        print(f"  {category:<18} INR {amount:,.2f}")
    print("\nSpending by date:")
    for date, amount in summary["dates"].items():
        print(f"  {date:%Y-%m-%d}          INR {amount:,.2f}")
    if len(summary["monthly"]) > 1:
        print("\nSpending by month:")
        for month, amount in summary["monthly"].items():
            print(f"  {month}              INR {amount:,.2f}")
    print("\n5 largest expenses:")
    for _, row in summary["top_five"].iterrows():
        print(f"  INR {row['amount']:,.2f}  {row['date']:%Y-%m-%d}  {row['category']} - {row['description']}")


def main():
    try:
        print_summary(calculate_summary(load_expenses()))
    except ValueError as exc:
        raise SystemExit(f"Error: {exc}") from exc


if __name__ == "__main__":
    main()


