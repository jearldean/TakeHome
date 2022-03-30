#!/usr/bin/python3.9
"""Server for Melon Tasting Reservations"""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db
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
    if "login_name" in session:
        return True
    else:
        return False


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""
    login_name = request.form["login_name"]
    password = request.form["password"]
    user = crud.get_user_by_login_name(login_name=login_name)

    if not user:
        flash("No one with that username found.")
        return redirect("/")
    if crud.does_password_match(user=user, password_from_form=password):
        session["login_name"] = user.login_name
        return redirect("/my_reservations")
    else:
        flash("Oops, password didn't match.")
        return redirect("/")


@app.route("/logout")
def logout():
    """Display homepage."""

    if "login_name" in session:
        del session["login_name"]
    flash("See you soon!")
    return redirect("/")


@app.route("/my_reservations")
def my_res():
    """Display homepage."""

    user = crud.get_user_by_login_name(login_name=session["login_name"])
    my_tastings = crud.get_my_reservations(user=user)
    print(my_tastings)
    return render_template('my_reservations.html', user=user, my_tastings=my_tastings,
                           user_logged_in=is_user_logged_in())


@app.route("/select_appointment", methods=["POST"])
def select_appointment():
    """Display homepage."""

    user = crud.get_user_by_login_name(login_name=session["login_name"])
    date = request.form["pick-date"]
    time1 = request.form["pick-time1"]
    time2 = request.form["pick-time2"]

    avaliable_times = crud.search_for_available_appointments(
        user, desired_day=date, start_time=min(time1, time2), end_time=max(time1, time2))

    return render_template('select_appointment.html',
                           avaliable_times=avaliable_times,
                           user_logged_in=is_user_logged_in())


@app.route("/specify_time_window")
def specify_time_window():
    """Display homepage."""
    min_date, max_date = crud.min_max_date_range()
    return render_template('specify_time_window.html',
                           min_date=min_date,
                           max_date=max_date,
                           user_logged_in=is_user_logged_in())


@app.route('/record_appointment', methods=['POST'])
def record_app():
    user = crud.get_user_by_login_name(login_name=session["login_name"])

    desired_appointment_id = request.form["record-it"]
    print('\n\n\n\n\n', desired_appointment_id)

    desired_appointment = crud.get_appointment_by_id(appointment_id=int(desired_appointment_id))

    if crud.can_user_book_this_reservation(user=user, desired_appointment=desired_appointment):
        flash("You got it!")
    else:
        flash(f"Could not get {'friday the 13th'}")

    return redirect("/my_reservations")


"""
Problem Statement: https://docs.google.com/document/d/1g5WMLwezVuGCNnZBafREobcDDst8PgxElGPHfk7EgRI/edit#
"""

if __name__ == "__main__":
    connect_to_db(app)
    # DebugToolbarExtension(app)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = False

    app.run(host="0.0.0.0", debug=True)
