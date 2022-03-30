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
* Password Encryption and Authentication
* Appointment Window is a variable to easily accommodate a change from half-hour appointments in the future.
* Unit Tests
* css
* Proposed Implementation for a Cancel Reservation Button, the only way to change a reservation.
* Seed Database Program
* Message for no Reservations Available includes a SELECT_AGAIN button to try again.

## 👎 Required Features not Included in First Commit
* readme.md (Now included 👍)
* Select Reservation Button does not work. (Now working 👍)
* Proposed Cancel Reservation Button does not work. (Now working 👍)
* Site Deployment (TODO)


________________

# Data Model

* **Users** are people who enjoy tasting melons.
* **Appointments** are time slots for tasting melons.
* **Reservations** are Appointments that are owned by a User.


## Schema
* Users
  * user_id, _int_  <span style="color:green">Primary Key</span>
  * login_name, _str_
  * hashed_password, _str_
* Appointments
  * appointment_id, _int_ <span style="color:blue">Primary Key</span>
  * appointment_date_time, _datetime object_
* Reservations
  * reservation_id, _int_ <span style="color:red">Primary Key</span>
  * user_id, _int_ <span style="color:green">Foreign Key</span>
  * appointment_id, _int_ <span style="color:blue">Foreign Key</span>


________________

# Design Choices

* model.py, a SQLAlchemy model for the schema above.
* crud.py contains functions for users, appointments and reservations.
* server.py is just simple flask routes. No time for fancy JavaScript.
* Database is PostgreSQL. When you got the best, don't mess with the rest.
* Unit Tests for many crud routines.
* seed_database.py offers several customizable settings:
  * SEED_APPOINTMENTS, number of days of future appointments to schedule.
  * APPOINTMENT_DURATION, minutes, flexible design for changes later.
  * SEED_USERS, number of fake users to create
    * Must have enough users to simulate some likely collisions.
  * SEED_RESERVATIONS, number of Reservations to create for EACH user.
* Including a Cancel button. It's the only way to change an appointment time.