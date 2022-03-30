# 🍉 🍈 Melon Tasting Reservations System 🍈 🍉
A Hackbright TakeHome Exercise


## 🍉 Required Features Included
* User Login
* Search Appointments
  * Date Picker
  * Optional Time Pickers
  * User is restricted to one reservation per calendar date.
  * Message for no Reservations Available within search parameters.
  * 48 pre-seeded reservation windows available per day.
* User Data is Preserved
* User can view their Reservations

## 🍉 Bonus Features Included
* Password Excryption and Authentication
* Appointment Window is a variable to easily accomodate a change from half-hour appointments in the future.
* Unit Tests
* css
* Proposed Implementation for a Cancel Reservation Button, the only way to change a reservation.
* Seed Database Program
* Message for no Reservations Available includes a SELECT_AGAIN button to try again.

## 👎 Required Features not Included in First Commit
* readme.md
* Select Reservation Button does not work.
* Proposed Cancel Reservation Button does not work.
* Site Deployment


________________

# Data Model

* **Users** are people who enjoy tasting melons.
* **Appointments** are time slots for tasting melons.
* **Reservaations** are Appointments that are owned by a User.


##Schema
* Users
  * user_id, _int_
  * login_name, _str_
  * hashed_password, _str_
* Appointments
  * appointment_id, _int_
  * appointment_date_time, _datetime object_
* Reservations
  * reservation_id, _int_
  * user_id, _int_
  * appointment_id, _int_


________________

# Design Choices

* model.py, a SQLAlchemy model for the schema above.
* crud.py contains functions for users, appointments and reservations.
* server.py is just simple flask routes. No time for fancy JavaScript.
* Database is PostgreSQL. When you got the best, don't mess with the rest.
* Unit Tests for every routine in crud.py.
* seed_database.py offers several customizable settings:
  * SEED_APPOINTMENTS, number of days of future appointments to schedule.
  * APPOINTMENT_DURATION, minutes, flexible design for changes later.
  * SEED_USERS = 50, number of fake users to create
    * Must have enough users to simulate some likely collisions.
  * SEED_RESERVATIONS, number of Reservations to create for EACH user.






