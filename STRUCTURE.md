# Project Structure

This project follows standard Python package conventions for clean code organization.

## Directory Layout

```
project/
├── src/                          # Main source code package
│   ├── __init__.py              # Package initialization
│   ├── config.py                # Configuration and environment variables
│   ├── csv_manager.py           # CSV loading, DOB parsing, birthday reminder logic
│   ├── data_loader.py           # JSON data loading (prices)
│   ├── llm_manager.py           # OpenAI LLM integration
│   ├── whatsapp_api.py          # WhatsApp API simulation/integration
│   ├── birthday_messenger.py    # Birthday message generation
│   ├── birthday_simulator.py    # Full birthday flow simulator with report generation
│   ├── reminders.py             # Birthday reminder update script
│   ├── main.py                  # Interactive LLM chat interface
│   └── server_flask.py          # Flask webhook server
├── tests/                        # Unit tests
│   ├── __init__.py
│   └── test_csv_manager.py      # Tests for CSV manager functions
├── data/                         # CSV data and reports (gitignored for large files)
│   ├── Data Almeera - leads_pwt.csv
│   ├── updated_leads.csv        # Generated on each reminder run
│   └── birthday_report_YYYYMMDD.csv  # Generated reports
├── Price List/                   # Pricelist JSON data
│   └── prices_august.json
├── docs/                         # Documentation
│   └── MILESTONE_01.md
├── configs/                      # Configuration files (reserved for future use)
├── .env                         # Environment variables (not committed)
├── .gitignore                   # Git exclusions
├── requirements.txt             # Python dependencies
├── runtime.txt                  # Python version (for deployment)
├── Procfile                     # Heroku deployment config
├── railway.json                 # Railway deployment config
├── render.yaml                  # Render deployment config
├── setup_production.py          # Production setup script
├── deployment_guide.md          # Deployment instructions
├── readme.md                    # Project overview
├── STRUCTURE.md                 # This file
├── main.py                      # Entry point wrapper (imports src.main)
├── reminders.py                 # Entry point wrapper (imports src.reminders)
├── birthday_messenger.py        # Entry point wrapper (imports src.birthday_messenger)
├── birthday_simulator.py        # Entry point wrapper (imports src.birthday_simulator)
└── server_flask.py              # Entry point wrapper (imports src.server_flask)
```

## Module Responsibilities

| Module | Purpose |
|--------|---------|
| `config.py` | Load `.env` and export API keys, paths |
| `csv_manager.py` | Load/save CSV files, parse dates, update birthday reminders |
| `data_loader.py` | Load JSON pricelist data |
| `llm_manager.py` | OpenAI client management, chat responses, content moderation |
| `whatsapp_api.py` | WhatsApp Cloud API calls (simulated if no token) |
| `birthday_messenger.py` | Generate birthday messages with LLM |
| `birthday_simulator.py` | Full flow: load CSV → update reminders → generate messages → simulate send → write report |
| `reminders.py` | Simple reminder update from CSV |
| `main.py` | Interactive chat loop for testing LLM |
| `server_flask.py` | Flask webhook endpoint for live WhatsApp integration |

## Running Scripts

All scripts can be run directly from the project root (entry point wrappers automatically import from `src/`):

```bash
# Update birthday reminders
python reminders.py

# Generate birthday messages (console output only)
python birthday_messenger.py

# Run full simulator with report generation
python birthday_simulator.py

# Interactive LLM chat
python main.py

# Flask webhook server
python server_flask.py
```

Or import directly from `src/`:

```python
from src.birthday_simulator import run_simulation
from src.csv_manager import load_csv, update_birthday_reminders_for_today
```

## Testing

Run unit tests with:

```bash
python -m pytest tests/
# or
python -m unittest tests.test_csv_manager
```

## Key Improvements

- **Separation of Concerns**: Core logic in `src/`, entry points at root
- **Reusability**: Import any module function directly: `from src.csv_manager import load_csv`
- **Testability**: Isolated `tests/` directory with standard unittest structure
- **Maintainability**: Clear module names and responsibilities
- **Deployment**: Standard Python package structure works with all major platforms (Heroku, Railway, Render, etc.)

## Deprecated Files

- `sheets_manager.py` (root) — Replaced by `src/csv_manager.py` for local testing
- `config.py`, `data_loader.py`, `llm_manager.py`, `whatsapp_api.py` (root) — Moved to `src/`

Old root versions will be removed after confirming all imports work from `src/`.
