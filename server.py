#!/usr/bin/python3.9
"""Server for Melon Tasting Reservations"""

from flask import Flask, render_template, request, flash, session, redirect
from model import Reservation, connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "itsasecret"
app.jinja_env.undefined = StrictUndefined

user_logged_in = None


@app.route("/")
def homepage():
    """Display homepage."""

    return render_template('homepage.html', user_logged_in=is_user_logged_in())


def is_user_logged_in():
    """Returns bool."""

    if "user_id" in session:
        return True
    else:
        return False


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    login_name = request.form["login_name"]
    password = request.form["password"]
    user = crud.get_user_by_login_name(login_name=login_name)

    if crud.does_password_match(user=user, password_from_form=password):
        session["user_id"] = user.user_id
        return redirect("/my_reservations")
    else:
        flash("Oops, Login Name and Password didn't match.")
        return redirect("/")

 
@app.route("/logout")
def logout():
    """Log out user."""

    if "user_id" in session:
        del session["user_id"]
    flash("See you soon!")
    return redirect("/")


@app.route("/my_reservations")
def my_reservations():
    """Display user's reservations."""

    user = crud.get_user_by_id(user_id=session["user_id"])
    my_reservations = crud.get_my_reservations(user=user)
    return render_template(
        'my_reservations.html', user=user, my_reservations=my_reservations,
        user_logged_in=is_user_logged_in())


@app.route("/select_appointment", methods=["GET"])
def select_appointment():
    """Users search for free appointments."""

    user = crud.get_user_by_id(user_id=session["user_id"])
    date = request.args["pick-date"]
    time1 = request.args["pick-time1"]
    time2 = request.args["pick-time2"]

    avaliable_times = crud.search_for_available_appointments(
        user, desired_day=date, start_time=min(time1, time2), end_time=max(time1, time2))

    return render_template('select_appointment.html',
                           avaliable_times=avaliable_times,
                           user_logged_in=is_user_logged_in())


@app.route("/specify_time_window")
def specify_time_window():
    """Input time search parameters."""

    min_date, max_date, _, max_date_raw = crud.min_max_date_range()
    return render_template('specify_time_window.html',
                           min_date=min_date,
                           max_date=max_date,
                           max_human_date = crud.format_human_date(max_date_raw),
                           user_logged_in=is_user_logged_in())


@app.route('/record_appointment', methods=['POST'])
def record_appointment():
    """Book a reservation"""

    user = crud.get_user_by_id(user_id=session["user_id"])
    desired_appointment_id = request.form['book_this_appointment']
    desired_appointment = crud.get_appointment_by_id(
        appointment_id=int(desired_appointment_id))
    human_reservation_datetime = crud.format_human_datetime(
        desired_appointment.appointment_date_time)

    if crud.can_user_book_this_reservation(user=user, desired_appointment=desired_appointment):
        flash(f"You got it! See you on {human_reservation_datetime}")
    else:
        flash(f"Sorry, We could not get you {human_reservation_datetime}")
    return redirect("/my_reservations")


@app.route('/cancel_reservation/<reservation_id>', methods=["GET", 'DELETE'])
def cancel_reservation(reservation_id):
    """Cancel a reservation."""

    crud.delete_reservation(reservation_id)
    return redirect("/my_reservations")


if __name__ == "__main__":
    connect_to_db(app)

    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = False

    app.run(host="0.0.0.0", port=5001, debug=True)
