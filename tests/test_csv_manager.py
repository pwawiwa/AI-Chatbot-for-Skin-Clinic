"""
Tests for csv_manager module
"""
import unittest
from datetime import datetime
from src.csv_manager import _parse_dob, update_birthday_reminders_for_today, get_rows_where_column_equals


class TestParseDOB(unittest.TestCase):
    """Test DOB parsing function"""
    
    def test_parse_dob_format_ddmmyyyy(self):
        result = _parse_dob("09/12/1990")
        self.assertEqual(result, (12, 9))
    
    def test_parse_dob_format_yyyymmdd(self):
        result = _parse_dob("1990-12-09")
        self.assertEqual(result, (12, 9))
    
    def test_parse_dob_format_ddmyyyy(self):
        result = _parse_dob("09-12-1990")
        self.assertEqual(result, (12, 9))
    
    def test_parse_dob_invalid(self):
        result = _parse_dob("invalid")
        self.assertIsNone(result)
    
    def test_parse_dob_empty(self):
        result = _parse_dob("")
        self.assertIsNone(result)


class TestBirthdayReminders(unittest.TestCase):
    """Test birthday reminder update logic"""
    
    def test_update_birthday_reminders_matches_today(self):
        rows = [
            {"Nama": "Alice", "Tanggal lahir": f"{datetime.now().day:02d}/{datetime.now().month:02d}/1990", "ULTAH REMINDER": ""},
            {"Nama": "Bob", "Tanggal lahir": "15/06/1985", "ULTAH REMINDER": ""},
        ]
        updated = update_birthday_reminders_for_today(rows, write_back_path=None)
        # Alice matches today, Bob doesn't
        self.assertEqual(updated, 1)
        self.assertEqual(rows[0]["ULTAH REMINDER"], "ULTAH HARI INI")
        self.assertEqual(rows[1]["ULTAH REMINDER"], "")
    
    def test_get_rows_where_column_equals(self):
        rows = [
            {"Nama": "Alice", "Status": "ULTAH HARI INI"},
            {"Nama": "Bob", "Status": ""},
            {"Nama": "Charlie", "Status": "ULTAH HARI INI"},
        ]
        result = get_rows_where_column_equals(rows, "Status", "ULTAH HARI INI")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["Nama"], "Alice")
        self.assertEqual(result[1]["Nama"], "Charlie")


if __name__ == '__main__':
    unittest.main()
