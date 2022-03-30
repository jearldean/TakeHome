"""Models for Melon Tasting Reservations"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    login_name = db.Column(db.String(256), unique=True, nullable=False)
    # It's extra credit; maybe we get here:
    hashed_password = db.Column(db.String, nullable=False)

    # reservations = a list of Reservation objects

    def __repr__(self):
        return f'{self.user_id}. {self.login_name}'


class Appointment(db.Model):
    """An appointment."""

    __tablename__ = 'appointments'

    appointment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    appointment_date_time = db.Column(db.DateTime, nullable=True)

    # reservations = a list of Reservation objects

    def __repr__(self):
        return f'{self.appointment_id}. {self.appointment_date_time}'


class Reservation(db.Model):
    """A reservation."""

    __tablename__ = 'reservations'

    reservation_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointments.appointment_id"))

    user = db.relationship("User", backref="reservations")
    appointment = db.relationship("Appointment", backref="reservations")

    def __repr__(self):
        return f'{self.reservation_id}. Expect {self.user.login_name} at {self.appointment.appointment_date_time}.'


def connect_to_db(flask_app, db_uri="postgresql:///reservations", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
