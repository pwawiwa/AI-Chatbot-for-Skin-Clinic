from .csv_manager import load_csv, update_birthday_reminders_for_today, get_rows_where_column_equals
from .data_loader import load_prices_data

# Local CSV data file
DATA_CSV = "data/Data Almeera - leads_pwt.csv"
PRICES_FILE = "data/prices_august.json"


def build_birthday_prompt(name):
    return (
        f"Buatkan pesan ucapan ulang tahun singkat dan manis untuk pasien bernama {name}. "
        "Gunakan Bahasa Indonesia yang girly, casual, elegan, dan hangat. "
        "Ajak pasien untuk menikmati Birthday Treat di Almeera dengan nada lembut (tanpa memaksa). "
        "Batasi 2-3 kalimat saja."
    )


def main():
    # Load treatment data for potential cross-sell in system prompt
    prices_data = load_prices_data(PRICES_FILE) or []

    rows = load_csv(DATA_CSV)
    if not rows:
        print("No data found in CSV.")
        return

    # Update reminders in-memory (and write an inspection CSV)
    update_birthday_reminders_for_today(rows, write_back_path="data/updated_leads.csv")

    # Fetch rows where ULT AH REMINDER == 'ULTAH HARI INI'
    rows = get_rows_where_column_equals(rows, "ULTAH REMINDER", "ULTAH HARI INI")
    if not rows:
        print("No birthdays today.")
        return

    print(f"Found {len(rows)} birthdays today. Generating messages...\n")

    for row in rows:
        # Support multiple possible name column headers
        name = row.get("Nama") or row.get("NAMA") or row.get("nama") or row.get("Name") or row.get("name") or "Kak"
        # try common phone header names
        phone = row.get("No. Whatsapp", row.get("No Whatsapp", row.get("No", "-")))

        # Build conversation for contextual LLM message
        # Lazy import LLM helper to avoid importing heavy libs at module import time
        try:
            from .llm_manager import get_llm_response
            messages = [{"role": "user", "content": build_birthday_prompt(name)}]
            response = get_llm_response(messages, prices_data)
        except Exception as e:
            response = f"[LLM not available for testing: {e}] Hello {name}, selamat ulang tahun!"
        print("==== Message ====")
        print(f"To: {phone} | Name: {name}")
        print(response)
        print()


if __name__ == "__main__":
    main()
