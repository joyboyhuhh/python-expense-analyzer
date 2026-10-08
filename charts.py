"""Create and save expense charts without opening a GUI."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from expense_analyzer import CSV_PATH, calculate_summary, load_expenses

CHART_DIR = Path(__file__).with_name("charts")


def main():
    try:
        summary = calculate_summary(load_expenses(CSV_PATH))
    except ValueError as exc:
        raise SystemExit(f"Error: {exc}") from exc
    CHART_DIR.mkdir(exist_ok=True)
    category_path = CHART_DIR / "spending_by_category.png"
    date_path = CHART_DIR / "spending_over_time.png"
    fig, ax = plt.subplots(figsize=(8, 5))
    summary["categories"].sort_values().plot(kind="barh", ax=ax, color="#4472C4")
    ax.set(title="Spending by Category", xlabel="Amount (₹)", ylabel="Category")
    fig.tight_layout()
    fig.savefig(category_path, dpi=150)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(9, 5))
    summary["dates"].plot(ax=ax, marker="o", color="#ED7D31")
    ax.set(title="Spending Over Time", xlabel="Date", ylabel="Amount (₹)")
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(date_path, dpi=150)
    plt.close(fig)
    print(f"Charts saved to {CHART_DIR}:\n  {category_path.name}\n  {date_path.name}")


if __name__ == "__main__":
    main()
