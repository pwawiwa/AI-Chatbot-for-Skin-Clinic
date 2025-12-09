import csv
from datetime import datetime
from typing import List, Dict, Tuple, Optional


def load_csv(file_path: str) -> List[Dict[str, str]]:
    try:
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = [dict(r) for r in reader]
            print(f"Loaded {len(rows)} rows from {file_path}")
            return rows
    except FileNotFoundError:
        print(f"Warning: CSV file not found: {file_path}")
        return []
    except Exception as e:
        print(f"Error loading CSV {file_path}: {e}")
        return []


def save_csv(file_path: str, rows: List[Dict[str, str]]) -> bool:
    if not rows:
        print("No rows to write.")
        return False
    try:
        # preserve field order from first row
        fieldnames = list(rows[0].keys())
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in rows:
                writer.writerow(r)
        print(f"Saved {len(rows)} rows to {file_path}")
        return True
    except Exception as e:
        print(f"Error writing CSV {file_path}: {e}")
        return False


def _parse_dob(raw: str) -> Optional[Tuple[int, int]]:
    if not raw:
        return None
    raw = raw.strip()
    # Try common formats
    formats = ('%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y', '%d %m %Y', '%d.%m.%Y')
    for fmt in formats:
        try:
            d = datetime.strptime(raw, fmt)
            return d.month, d.day
        except Exception:
            continue
    # Try split by non-digit
    import re
    parts = re.split(r'\D+', raw)
    if len(parts) >= 2:
        try:
            d = int(parts[0])
            m = int(parts[1])
            # heuristic: if first > 12 then assume day/month -> swap
            if d > 12:
                return m, d
            return m, d
        except Exception:
            return None
    return None


def update_birthday_reminders_for_today(rows: List[Dict[str, str]],
                                        dob_field: str = 'Tanggal lahir',
                                        reminder_field: str = 'ULTAH REMINDER',
                                        bulan_field: str = 'BULAN',
                                        tanggal_field: str = 'TANGGAL',
                                        write_back_path: Optional[str] = None) -> int:
    """Set `reminder_field` to 'ULTAH HARI INI' for matching birthdays.
    Operates on list of dicts and optionally writes back to CSV if `write_back_path` provided.
    Returns number of rows changed.
    """
    from datetime import datetime

    today = datetime.now()
    today_m = today.month
    today_d = today.day
    updated = 0

    for r in rows:
        mm = None
        dd = None

        raw = r.get(dob_field, '')
        parsed = _parse_dob(raw)
        if parsed:
            mm, dd = parsed

        # fallback to separate columns
        if (mm is None or dd is None):
            try:
                b = r.get(bulan_field, '')
                t = r.get(tanggal_field, '')
                if b and t:
                    mm = int(b)
                    dd = int(t)
            except Exception:
                pass

        target = 'ULTAH HARI INI' if (mm == today_m and dd == today_d) else ''
        current = r.get(reminder_field, '')
        if (current or '') != target:
            r[reminder_field] = target
            updated += 1

    if write_back_path:
        # ensure all rows have same keys (add missing header keys if needed)
        # collect union of keys
        all_keys = []
        for r in rows:
            for k in r.keys():
                if k not in all_keys:
                    all_keys.append(k)
        # normalize rows to include all keys
        normalized = []
        for r in rows:
            nr = {k: (r.get(k, '') or '') for k in all_keys}
            normalized.append(nr)
        save_csv(write_back_path, normalized)

    print(f"Updated {updated} rows for birthday reminders (in-memory).")
    return updated


def get_rows_where_column_equals(rows: List[Dict[str, str]], column_name: str, expected_value: str) -> List[Dict[str, str]]:
    return [r for r in rows if str(r.get(column_name, '')).strip() == str(expected_value).strip()]
