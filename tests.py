import unittest
from utils import validate_amount, validate_date

class TestFinanceApp(unittest.TestCase):
    def test_validation(self):
        self.assertTrue(validate_amount("100.50"))
        self.assertFalse(validate_amount("abc"))
        self.assertTrue(validate_date("2026-01-03"))
        self.assertFalse(validate_date("31-12-2026"))

if __name__ == "__main__":
    unittest.main()
