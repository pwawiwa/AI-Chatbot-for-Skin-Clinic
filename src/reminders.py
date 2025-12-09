from .csv_manager import load_csv, update_birthday_reminders_for_today, save_csv

# Local CSV data file
DATA_CSV = "data/Data Almeera - leads_pwt.csv"


def main():
    rows = load_csv(DATA_CSV)
    if not rows:
        print("No data loaded; ensure the CSV path is correct.")
        return

    # Update in-memory and write an updated CSV for inspection
    updated = update_birthday_reminders_for_today(rows, write_back_path="data/updated_leads.csv")
    print(f"Done. Rows updated: {updated}")


if __name__ == "__main__":
    main()
