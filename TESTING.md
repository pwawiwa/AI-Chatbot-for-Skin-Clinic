# TESTING - Quick verification checklist

This file contains simple steps to verify each major feature locally.

Prerequisites
- Python 3.8+
- Virtual environment activated (`source .venv/bin/activate`)
- `.env` present in project root with `OPENAI_API_KEY` if you want real LLM responses

1) Update birthday reminders (CSV)

- Command:
```
python scripts/reminders.py
```
- Expected: `data/updated_leads.csv` is written and output prints how many rows updated.

2) Run full birthday simulator (generate messages + simulated sends)

- Command:
```
python scripts/birthday_simulator.py
```
- Expected:
  - `data/birthday_report_YYYYMMDD.csv` is created
  - Console prints `Found X target(s) for today.` and `Wrote report to ...`

3) Generate birthday messages (console only)

- Command:
```
python scripts/birthday_messenger.py
```
- Expected: Messages printed to console for each `ULTAH HARI INI` row.

4) Interactive LLM chat (terminal)

- Command:
```
python scripts/main.py
```
- What it does: opens an interactive loop. Type a message and press Enter to send it to the LLM. Type `exit` to quit.
- Notes: If `OPENAI_API_KEY` is present in `.env`, the real LLM will be used; otherwise a fallback response will be shown.

5) Run the Flask webhook server (local testing)

- Command:
```
python scripts/server_flask.py
```
- Expected: Server starts (port 8080 by default).
- For webhook testing, POST a simulated payload to `/webhook`.

6) Run unit tests

- Command:
```
python -m pytest tests/
```

Troubleshooting
- If modules fail to import, ensure you run commands from the project root so Python can resolve `src/`.
- If LLM calls fail, confirm `OPENAI_API_KEY` is valid and the environment has network access.

Contact
- If anything fails, run the failing command and paste the console output here.


.venv/bin/python scripts/birthday_simulator.py
.venv/bin/python scripts/main.py