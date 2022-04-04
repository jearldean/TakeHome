"""Tests for the Melon Tasting Reservations"""

import unittest

from server import app
from model import db, connect_to_db
import crud
import seed_database


class TestReservationsDB(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """This runs before every def test_* function."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(flask_app=app, db_uri=f"postgresql:///test_reservations")
        db.create_all()

        seed_database.SEED_APPOINTMENTS = 3  # days
        seed_database.APPOINTMENT_DURATION = 60  # mins
        seed_database.SEED_USERS = 3
        seed_database.SEED_RESERVATIONS = 10
        seed_database.POSSIBLE_PASSWORDS = ['secret', 'secret', 'secret']
        seed_database.seed_appointments()
        seed_database.seed_users_and_reservations()

    def test_appointments(self):
        """Tests for appointment crud"""

        # Create all the appointments promised:
        minutes_of_window = seed_database.SEED_APPOINTMENTS * 60 * 24
        number_of_windows = minutes_of_window / seed_database.APPOINTMENT_DURATION
        self.assertEqual(number_of_windows + 1, len(crud.get_appointments()))

        # No duplicate appointment slots:
        appointment_date_times = [
            appointment.appointment_date_time for appointment in crud.get_appointments()]
        self.assertFalse(self.are_there_dupes(a_list=appointment_date_times))

    def test_users(self):
        """Tests for user crud"""
        
        for i in range(seed_database.SEED_USERS):
            user_number = i + 1
            user = crud.get_user_by_login_name(login_name=f'Melon Taster {user_number}')

            # Your user_id is in your seed_database login_name:
            self.assertEqual(user_number, user.user_id)

            # Proper bcrypt passwords begin with '$2_$' with _ indicating the bcrypt version.
            self.assertEqual('$2b$', user.hashed_password[:4])

            # Password should match the only password choice:
            self.assertTrue(crud.does_password_match(
                user=user, password_from_form='secret'))

            # Password should not match any other word:
            self.assertFalse(crud.does_password_match(
                user=user, password_from_form='not a secret'))

            # login_names are unique; Should not be allowed to create a duplicate login_name:
            self.assertFalse(crud.check_then_create_user(
                login_name=f'Melon Taster {user_number}', password="xxx"))

            # Can't have more than 1 reservation per user per calendar day:
            my_reservation_dates = crud.get_my_reservations(user=user, human_readable=False)
            if my_reservation_dates:
                self.assertFalse(self.are_there_dupes(a_list=my_reservation_dates))

        # A new, unique login_name CAN be created:
        self.assertTrue(crud.check_then_create_user(
            login_name='Melon Taster 3.14159', password="pi"))

        # No duplicate login_names:
        login_names = [user.login_name for user in crud.get_users()]
        self.assertFalse(self.are_there_dupes(a_list=login_names))

    def test_reservations(self):
        """Tests for reservation crud"""

        # No 2 reservations can EVER occupy the same time window:
        reservation_appointment_ids = [res.appointment_id for res in crud.get_reservations()]
        self.assertFalse(self.are_there_dupes(a_list=reservation_appointment_ids))

    @staticmethod
    def are_there_dupes(a_list):
        """There are many columns where we can not allow collisions in data."""

        if len(a_list) == len(set(a_list)):
            return False
        else:
            return True

    def tearDown(self):
        """This runs after every def test_* function."""

        db.session.close()
        # Test Data is purged at the end of each test:
        db.drop_all()


if __name__ == "__main__":
    unittest.main()  # pytest --tb=long
