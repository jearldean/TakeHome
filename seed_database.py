"""Script to seed database for Melon Tasting Reservations"""

import os
from random import choice
from datetime import datetime, timedelta, date

import crud
import model
import server

DB_NAME = 'reservations'
SEED_APPOINTMENTS = 30  # days. One Month of selectable appointment slots.
APPOINTMENT_DURATION = 30  # mins, flexible design for changes later.
SEED_USERS = 50  # 48 available appointment slots per day;
# must have enough users to create some likely collisions.
SEED_RESERVATIONS = 10
POSSIBLE_PASSWORDS = ['sweet', 'juicy']


def seed_database():
    os.system(f"dropdb {DB_NAME}")  # This is just like:  $ dropdb reservations
    os.system(f"createdb {DB_NAME}")

    model.connect_to_db(server.app)
    model.db.create_all()

    seed_appointments()
    seed_users_and_reservations()


def seed_appointments():
    """Create SEED_APPOINTMENTS days worth of APPOINTMENT_DURATION appointments."""

    tomorrow_at_midnight = datetime.combine((date.today() + timedelta(days=1)), datetime.min.time())
    end_date = tomorrow_at_midnight + timedelta(days=SEED_APPOINTMENTS)
    count_appointments = 0
    appointment_date_time = tomorrow_at_midnight
    while appointment_date_time < end_date:
        appointment_date_time = tomorrow_at_midnight + timedelta(minutes=APPOINTMENT_DURATION * count_appointments)
        new_appointment = crud.create_appointment(appointment_date_time)
        model.db.session.add(new_appointment)
        count_appointments += 1
    model.db.session.commit()


def seed_users_and_reservations():
    """Create SEED_USERS users and SEED_RESERVATIONS reservations."""

    for n in range(SEED_USERS):
        login_name = 'Melon Taster ' + str(n + 1)
        password = choice(POSSIBLE_PASSWORDS)
        new_user = crud.create_user(login_name, password)
        model.db.session.add(new_user)

        all_appointments = crud.get_appointments()
        for _ in range(SEED_RESERVATIONS):
            random_appointment = choice(all_appointments)
            crud.can_user_book_this_reservation(user=new_user, desired_appointment=random_appointment)


if __name__ == '__main__':
    """Will connect you to the database when you run seed_database.py interactively"""

    from server import app

    model.connect_to_db(app)
