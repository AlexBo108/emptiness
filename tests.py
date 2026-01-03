import unittest
from models import FinancialOperation
from utils import validate_amount

class TestFinance(unittest.TestCase):
    def test_operation_creation(self):
        op = FinancialOperation(100, "Еда", "2026-01-01", "Обед")
        self.assertEqual(op.amount, 100.0)

    def test_validation(self):
        self.assertTrue(validate_amount("150.50"))
        self.assertFalse(validate_amount("abc"))

if __name__ == "__main__":
    unittest.main()
