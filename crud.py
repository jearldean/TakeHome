"""CRUD operations for Melon Tasting Reservations"""

import bcrypt
from datetime import date
from model import db, connect_to_db, User, Appointment, Reservation
from sqlalchemy import func

""" -=-=-=-=-=-=-=-=-=-=-=-=-=-=- USERS -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- """


def create_user(login_name: str, password: str) -> User:
    """Create and return a new user."""

    user = User(login_name=login_name, hashed_password=hash_it(password))
    db.session.add(user)
    return user


def get_users() -> User:
    """Return all users."""

    return User.query.all()


def get_user_by_id(user_id: int) -> User:
    """Return a user by primary key."""

    return User.query.get(user_id)


def get_user_by_login_name(login_name: str) -> User:
    """Return a user by login_name."""

    return User.query.filter(User.login_name == login_name).first()


def check_then_create_user(login_name: str, password: str):  # -> Optional[bool, ]
    """Create and return a new user if login_name not in use."""

    if does_this_user_exist_already(login_name=login_name):
        return False
    else:
        new_user = create_user(login_name=login_name, password=password)
        db.session.commit()
        return new_user


def does_this_user_exist_already(login_name: str) -> bool:
    """Return a boolean we can use for the if-statement in server.py."""

    if get_user_by_login_name(login_name=login_name):
        return True
    else:
        return False


def does_password_match(user: User, password_from_form: str) -> bool:
    """Check hashed password. Returns boolean."""

    if bcrypt.checkpw(
            password_from_form.encode('utf8'),
            user.hashed_password.encode('utf8')):
        print("Password matched!")
        return True
    else:
        print("Password did not match.")
        return False


def hash_it(password: str) -> str:
    """Hash and Salt plaintext password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf8'), salt)
    hashed_password = hashed.decode('utf8')
    return hashed_password


""" -=-=-=-=-=-=-=-=-=-=-=-=-=-=- APPOINTMENTS -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- """


def create_appointment(appointment_date_time):
    """Create and return a new appointment."""

    appointment = Appointment(appointment_date_time=appointment_date_time)

    return appointment


def get_appointments():
    """Return all appointments."""

    return Appointment.query.all()


def get_appointment_by_id(appointment_id):
    """Return one appointment."""

    return Appointment.query.get(appointment_id)


def search_for_available_appointments(user, desired_day, start_time=None, end_time=None):
    """Return all available appointments. desired_day must be in time_format = '%Y-%m-%d'

    start_time, end_time are optional.
    """

    if does_user_already_have_a_reservation_this_day(user, desired_day):
        return False  # Day not eligible for consideration.

    if not start_time:
        start_time = "00:00:00"
    if not end_time:
        end_time = "23:59:59"
    search_start = f"{desired_day} {start_time}"
    search_end = f"{desired_day} {end_time}"

    appointments_list = db.session.query(Appointment).filter(
        Appointment.appointment_id.not_in(db.session.query(Reservation.appointment_id))).filter(
        Appointment.appointment_date_time <= search_end).filter(
        Appointment.appointment_date_time >= search_start).order_by(
        Appointment.appointment_date_time).all()

    if appointments_list:
        results_dict = format_appointments_list(appointments_list)
        return results_dict
        # These are Appointment objects. Use strftime to display them pretty in the UI if that is the destination.
    else:
        return False  # None found on that day or within those times.


def format_appointments_list(appointments_list):
    results_dict = {}
    for jj in appointments_list:
        results_dict[jj.appointment_id] = jj.appointment_date_time.strftime('%A, %B %-d, %Y at %-I:%M %p')
    return results_dict


def min_max_date_range():
    today = date.today().strftime('%Y-%m-%d')
    print(today)
    min_date = db.session.query(func.min(Appointment.appointment_date_time)).first()[0].strftime('%Y-%m-%d')
    # Can't schedule things in the past:
    min_ = max(today, min_date)

    max_ = db.session.query(func.max(Appointment.appointment_date_time)).first()[0].strftime('%Y-%m-%d')
    return min_, max_


""" -=-=-=-=-=-=-=-=-=-=-=-=-=-=- RESERVATIONS -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- """


def create_reservation(user, appointment):
    """Create and return a new reservation."""
    reservation = Reservation(user=user, appointment=appointment)
    db.session.add(reservation)
    db.session.commit()

    return reservation


def get_reservations():
    """Return all reservations."""

    return Reservation.query.all()


def delete_reservation(reservation_id):
    """Delete a row from reservations."""
    reservation = Reservation.query.get(reservation_id)
    db.session.delete(reservation)
    db.session.commit()


def can_user_book_this_reservation(user, desired_appointment):
    """There are 2 reasons to deny a user an appointment:

    1. User can have only one appointment per calendar day. Will have to delete it to change an appointment ona day.
    2. Appointment is already taken by another user.
    """
    if not does_user_have_a_conflict_with_desired_appointment(
            user, desired_appointment) and not does_this_reservation_exist_already(desired_appointment):
        return create_reservation(user, desired_appointment)
    else:
        # No reservation for you!
        return False


def does_user_have_a_conflict_with_desired_appointment(user, desired_appointment):
    """ """
    time_format = '%Y-%m-%d'
    desired_day = desired_appointment.appointment_date_time.strftime(time_format)
    return does_user_already_have_a_reservation_this_day(user, desired_day)


def does_user_already_have_a_reservation_this_day(user, desired_day):
    """desired_day must be in time_format = '%Y-%m-%d'"""
    time_format = '%Y-%m-%d'
    my_reservations = get_my_reservations(user, strftime_format=time_format)
    my_reservation_dates = [qq[0] for qq in my_reservations]

    if my_reservation_dates and desired_day in my_reservation_dates:
        return True
    else:
        return False


def does_this_reservation_exist_already(desired_appointment):
    """Return a boolean we can use for the if-statement in can_user_book_this_reservation."""

    if Reservation.query.filter(Reservation.appointment_id == desired_appointment.appointment_id).first():
        return True  # Time slot already in use
    else:
        return False


def get_my_reservations(user, strftime_format='%A, %B %-d, %Y at %-I:%M %p'):
    """Show all reservations for a user in human-readable format."""
    my_reservations = db.session.query(Appointment.appointment_date_time, Reservation.reservation_id).filter(
        Reservation.user_id == user.user_id).filter(
        Reservation.appointment_id == Appointment.appointment_id).order_by(
        Appointment.appointment_date_time).all()
    list_of_tuples = [(jj[0].strftime(strftime_format), jj[1]) for jj in my_reservations]
    return list_of_tuples


if __name__ == '__main__':
    """Will connect you to the database when you run crud.py interactively"""
    from server import app

    connect_to_db(app)
