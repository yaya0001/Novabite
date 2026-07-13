import os
import tempfile
import unittest

from Tools import loyalty


class LoyaltySystemTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        loyalty.STATE_FILE = os.path.join(self.temp_dir.name, "loyalty_state.json")
        loyalty._reset_state_for_tests()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_no_discount_before_three_visits(self):
        status = loyalty.get_loyalty_status("customer-1")
        self.assertEqual(status["visits"], 0)
        self.assertFalse(status["discount_available"])

    def test_discount_becomes_available_after_three_visits(self):
        loyalty.record_visit("customer-1")
        loyalty.record_visit("customer-1")
        loyalty.record_visit("customer-1")

        status = loyalty.get_loyalty_status("customer-1")
        self.assertEqual(status["visits"], 3)
        self.assertTrue(status["discount_available"])

    def test_discount_redeem_consumes_one_reward(self):
        for _ in range(3):
            loyalty.record_visit("customer-1")

        result = loyalty.redeem_discount("customer-1", 1000)
        self.assertIn("10%", result)
        self.assertIn("900.0", result)

        status = loyalty.get_loyalty_status("customer-1")
        self.assertEqual(status["available_discounts"], 0)


if __name__ == "__main__":
    unittest.main()
