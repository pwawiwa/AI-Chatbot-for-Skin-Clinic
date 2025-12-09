"""
sheets_manager.py

This project no longer uses Google Sheets integration for local testing.
The original `sheets_manager` has been replaced by `csv_manager.py` which
operates on local CSV files in `data/` for reminders and testing.

If you still need Google Sheets integration, re-add the implementation
and the required credentials, but be careful not to commit sensitive keys.
"""

raise ImportError("sheets_manager is deprecated in this workspace; use csv_manager instead")
