import os
import tempfile
import unittest

from Tools import booking


class BookingToolTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        booking.STATE_FILE = os.path.join(self.temp_dir.name, "booking_state.json")
        booking._reset_state_for_tests()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_check_availability_reports_full_capacity(self):
        result = booking.check_restaurant_availability("Cairo", "2099-01-01", "19:00")
        self.assertIn("50", result)
        self.assertIn("available", result.lower())

    def test_booking_confirms_and_reduces_availability(self):
        confirmation = booking.book_restaurant_table(
            location="Cairo",
            party_size=4,
            date="2099-01-01",
            time_slot="19:00",
            customer_name="Alice",
        )
        self.assertIn("confirmed", confirmation.lower())

        availability = booking.check_restaurant_availability("Cairo", "2099-01-01", "19:00")
        self.assertIn("49", availability)

    def test_booking_rejects_when_capacity_is_exhausted(self):
        for _ in range(50):
            booking.book_restaurant_table(
                location="Cairo",
                party_size=2,
                date="2099-01-02",
                time_slot="20:00",
                customer_name="Guest",
            )

        rejection = booking.book_restaurant_table(
            location="Cairo",
            party_size=2,
            date="2099-01-02",
            time_slot="20:00",
            customer_name="Overflow",
        )

        self.assertIn("not enough", rejection.lower())


if __name__ == "__main__":
    unittest.main()
