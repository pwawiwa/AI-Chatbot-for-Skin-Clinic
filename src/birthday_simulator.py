import csv
from datetime import datetime
from pathlib import Path

from .csv_manager import load_csv, update_birthday_reminders_for_today, get_rows_where_column_equals
from .birthday_messenger import build_birthday_prompt
from .data_loader import load_prices_data
from . import whatsapp_api

# Use same CSV and prices paths as other scripts
DATA_CSV = "data/Data Almeera - leads_pwt.csv"
PRICES_FILE = "data/prices_august.json"
REPORT_DIR = Path("outputs")
REPORT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def run_simulation(write_report: bool = True):
    rows = load_csv(DATA_CSV)
    if not rows:
        print("No data loaded; ensure the CSV path is correct.")
        return

    # Update reminders (writes an inspection CSV)
    updated = update_birthday_reminders_for_today(rows, write_back_path=str(REPORT_DIR / "updated_leads.csv"))
    print(f"Updated {updated} rows (reminder flags).")

    # Select today's birthdays
    targets = get_rows_where_column_equals(rows, "ULTAH REMINDER", "ULTAH HARI INI")
    print(f"Found {len(targets)} target(s) for today.")

    # Load prices for contextual LLM (optional)
    prices_data = load_prices_data(PRICES_FILE) or []

    # Prepare report rows
    report_rows = []

    # Lazy import LLM call here to allow safe operation even if OpenAI not configured
    try:
        from .llm_manager import get_llm_response
    except Exception as e:
        get_llm_response = None
        print(f"LLM manager not available: {e}")

    for r in targets:
        # Support multiple possible name column headers (case variations)
        name = r.get("Nama") or r.get("NAMA") or r.get("nama") or r.get("Name") or r.get("name") or "Kak"
        phone = r.get("No. Whatsapp", r.get("No Whatsapp", r.get("No", "-")))

        # Build message via LLM if available, else simple template
        msg = None
        if get_llm_response:
            try:
                user_msg = build_birthday_prompt(name)
                messages = [{"role": "user", "content": user_msg}]
                msg = get_llm_response(messages, prices_data)
            except Exception as e:
                msg = f"[LLM Error] Selamat ulang tahun, {name}!"
        else:
            msg = f"Selamat ulang tahun, Kak {name}! Semoga hari istimewa ini menyenangkan."

        # Build outgoing text that will actually be sent/printed: "Kak <first_name> <message>"
        # Avoid duplicating 'Kak' if the name already begins with it
        cleaned_name = (name or "Kak").strip()
        first_name = cleaned_name.split()[0] if cleaned_name else "Kak"
        if first_name.lower().startswith("kak"):
            outgoing_text = f"{cleaned_name} {msg}"
        else:
            outgoing_text = f"Kak {first_name} {msg}"

        # Simulate send via whatsapp_api (function will print SIMULATED if no token is set)
        sent_ok, resp = whatsapp_api.send_text_message(phone, outgoing_text)

        # If the whatsapp api returned a simulated-send message, mark the report clearly
        sent_field = None
        try:
            if isinstance(resp, str) and resp.startswith("SIMULATED"):
                sent_field = "SIMULATED"
            else:
                sent_field = str(sent_ok)
        except Exception:
            sent_field = str(sent_ok)

        report_rows.append({
            "Timestamp": datetime.now().isoformat(),
            "Nama": name,
            "Phone": phone,
            "Message": msg,
            "OutgoingMessage": outgoing_text,
            "Sent": sent_field,
            "SendResponse": resp,
        })

    if write_report:
        report_path = REPORT_DIR / f"birthday_report_{datetime.now().strftime('%Y%m%d')}.csv"
        # write CSV
        if report_rows:
            keys = list(report_rows[0].keys())
            with open(report_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                for rr in report_rows:
                    writer.writerow(rr)
            print(f"Wrote report to {report_path}")
        else:
            print("No report rows to write.")

    # Print short summary
    for rr in report_rows:
        print(f"To: {rr['Nama']} ({rr['Phone']}) — Sent: {rr['Sent']}")

    return report_rows


if __name__ == '__main__':
    run_simulation()
