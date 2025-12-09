# README.md: Beauty Clinic WhatsApp Chatbot

This project is a WhatsApp-based chatbot for a beauty clinic (klinik kecantikan). It handles customer inquiries, provides information on services and pricelist (daftar harga), and responds intelligently using an LLM (Large Language Model). Currently, the core chatbot and birthday reminder features are implemented. Additional features like doctor forwarding and order management are planned.

The chatbot uses Flask as the web server, WhatsApp Cloud API for messaging, and OpenAI's LLM. For local testing, WhatsApp sends are simulated. Data like API keys are stored in `.env`. All data is stored locally (CSVs in `data/` and pricelist JSON in `Price List/`).

## Project Structure

```
project/
├── src/                          # Main source code (all Python modules)
│   ├── config.py                 # Configuration & environment variables
│   ├── csv_manager.py            # CSV loading, DOB parsing, birthday reminders
│   ├── data_loader.py            # JSON data loading (pricelist)
│   ├── llm_manager.py            # OpenAI LLM integration
│   ├── whatsapp_api.py           # WhatsApp API (simulated when no credentials)
│   ├── birthday_messenger.py     # Birthday message generation
│   ├── birthday_simulator.py     # Full flow simulator with report
│   ├── reminders.py              # Birthday reminder updates
│   ├── main.py                   # Interactive LLM chat
│   └── server_flask.py           # Flask webhook server
├── tests/                        # Unit tests
│   └── test_csv_manager.py       # Tests for CSV functions
├── data/                         # CSV data & generated reports
│   ├── Data Almeera - leads_pwt.csv  # Patient list with birthdays
│   ├── updated_leads.csv         # Generated on each reminder run
│   └── birthday_report_*.csv     # Generated reports
├── Price List/                   # Pricelist JSON data
│   └── prices_august.json
├── docs/                         # Documentation
├── configs/                      # Future configuration files
├── .env                          # Environment variables (not committed)
├── requirements.txt              # Python dependencies
├── reminders.py                  # Entry point: run birthday reminders
├── birthday_messenger.py         # Entry point: generate birthday messages
├── birthday_simulator.py         # Entry point: full simulator with report
├── main.py                       # Entry point: interactive LLM chat
├── server_flask.py               # Entry point: Flask webhook server
└── STRUCTURE.md                  # Detailed structure & module documentation
```

**Key directories:**
- **src/**: All Python modules (importable and testable)
- **tests/**: Unit tests for core functions
- **data/**: CSV patient data and generated reports
- **Price List/**: Treatment pricelist (JSON)

## Prerequisites

- Python 3.8+ installed
- OpenAI API key (for LLM responses)
- Optional: WhatsApp Business API token (for real sends; without it, sends are simulated)

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repo-url>
   cd AI-Chatbot-for-Skin-Clinic
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure .env**:
   Create `.env` in the project root with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   WHATSAPP_TOKEN_ACCESS=your_whatsapp_token  # Optional (for real sends)
   PHONE_NUMBER=your_phone_number_id            # Optional (for real sends)
   WHATSAPP_VERIFY_TOKEN=your_verify_token
   WHATSAPP_APP_SECRET=your_app_secret
   ```
   
   **Note**: Without `WHATSAPP_TOKEN_ACCESS` and `PHONE_NUMBER`, WhatsApp sends will be simulated (printed to console).

5. **Verify Setup**:
   ```bash
   python scripts/reminders.py
   ```
   This should load the CSV and print "Rows updated: X".

6. **Set Up WhatsApp Webhook**:
   - In Meta Developers portal: Configure webhook URL (from Ngrok) in WhatsApp > Configuration > Webhooks.
   - Subscribe to "messages" event.
   - Add test phone numbers to avoid "Recipient not in allowed list" error.

## Running the Application

### Birthday Reminder Features (Testing Level)

**1. Update birthday reminders from CSV:**
```bash
python scripts/reminders.py
```
Loads `data/Data Almeera - leads_pwt.csv`, updates the `ULTAH REMINDER` column for today's birthdays, and writes `data/updated_leads.csv`.

**2. Generate birthday messages (console output):**
```bash
python scripts/birthday_messenger.py
```
Generates personalized birthday messages using OpenAI LLM (with fallback if unavailable) for all patients with `ULTAH REMINDER == "ULTAH HARI INI"`.

**3. Run full simulator with report generation:**
```bash
python scripts/birthday_simulator.py
```
Runs the complete flow: load CSV → update reminders → generate messages → simulate WhatsApp sends → write report.
Outputs:
- `data/updated_leads.csv` — updated patient list with reminder flags
- `data/birthday_report_YYYYMMDD.csv` — report with timestamp, name, phone, message, send status

### LLM Chat Testing

**Interactive chat loop:**
```bash
python scripts/main.py
```
Start an interactive conversation with the LLM. Type 'exit' to quit. Messages are moderated via OpenAI's moderation API.

### WhatsApp Webhook Server (Production)

**Start Flask server:**
```bash
python scripts/server_flask.py
```
Runs on `http://0.0.0.0:8080` (port configurable via `PORT` env var).

**For live integration:**
1. Set `WHATSAPP_TOKEN_ACCESS` and `PHONE_NUMBER` in `.env`
2. Configure your WhatsApp Business account webhook to point to your server
3. Server will handle incoming messages and send LLM responses via WhatsApp API

### Running Tests

```bash
python -m pytest tests/
# or
python -m unittest tests.test_csv_manager
```

## Current Features

- ✅ **Birthday Reminders**: Parse `Tanggal lahir` from CSV, identify today's birthdays, update reminder flags
- ✅ **Message Generation**: Use OpenAI LLM to create personalized birthday greetings in Indonesian
- ✅ **Report Generation**: CSV output of all reminders sent today
- ✅ **WhatsApp Simulation**: Simulated sends for testing (no token required)
- ✅ **LLM Chat**: Interactive conversation testing with content moderation
- ✅ **Webhook Server**: Flask endpoint for live WhatsApp integration
- ✅ **CSV Data**: Local patient and pricelist data management

## Planned Features

- Doctor forwarding for complex queries
- Order management and treatment scheduling
- Appointment reminders via WhatsApp

## Troubleshooting

- **ImportError on `from src.XXX` when running scripts**: Make sure you're running scripts from the project root directory.
- **No birthdays found today?**: Check the `Tanggal lahir` column in your CSV — supported formats: `DD/MM/YYYY`, `YYYY-MM-DD`, etc.
- **LLM responses are generic fallback messages?**: Set `OPENAI_API_KEY` in `.env` with a valid OpenAI API key.
- **WhatsApp sends not working?**: If `WHATSAPP_TOKEN_ACCESS` is not set, sends will be simulated (printed to console).
- **Flask server won't start?**: Check that port 8080 is available or set `PORT` env var to a different port.

## Project Documentation

- **STRUCTURE.md** — Detailed project structure, module responsibilities, and import patterns
- **docs/MILESTONE_01.md** — Project milestones and historical overview
- **deployment_guide.md** — Deployment instructions for Heroku, Railway, Render

## Development Workflow

1. **Make changes to modules in `src/`**
2. **Run tests**: `python -m pytest tests/` or `python -m unittest tests.test_csv_manager`
3. **Test entry points**: `python reminders.py`, `python birthday_simulator.py`, etc.
4. **Verify imports**: `python -c "from src.XXX import YYY; print('OK')"`
5. **Commit changes**: All Python code is in `src/`, entry points are thin wrappers