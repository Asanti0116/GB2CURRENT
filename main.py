import os
import psycopg2

from flask import Flask, redirect, url_for, render_template, request, session, flash, g
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from forms import UserAddForm, LoginForm, NotesForm
from models import db, connect_db, Users, Notes
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate


CURR_USER_KEY = "curr_user"

app = Flask(__name__)


# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:Pickles1011!@localhost:5432/gym_buddy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
migrate = Migrate(app, db)


app.config['SECRET_KEY'] = "shhh-don't-tell-anyone"





########################################################################################################
# User signup/login/logout

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = Users.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/')
def index():
   conn = psycopg2.connect("postgresql://postgres:Pickles1011!@localhost:5432/gym_buddy")
   return 'it works'


# def home():
  # return render_template('index.html')


@app.route("/user")
def user():
  if "user" in session:
    user = session["user"]
    return render_template("user.html", user=user)
  else:
    flash("You are not logged in!")
    return redirect(url_for("login"))


@app.route("/exercise-of-the-day")
def exercise_of_the_day():
  return render_template('exercise-of-the-day.html')


@app.route("/motivation")
def motivation():
  return render_template("motivation.html")


@app.route("/workouts", methods=['GET'])
def workouts():
  return render_template("workouts.html")


@app.route("/notes")
def notes():
  return render_template("notes.html")


###### AUTH ROUTES


@app.route('/login', methods=["POST", "GET"])
def login():
  if request.method == "POST":
    session.permanent = True
    user = request.form["nm"]
    session["user"] = user

    found_user = user.query.filter_by(name=user).first()
    if found_user:
      session["email"] = found_user.email
    else:
      usr = user(user, "")
      db.session.add(usr)
      db.commit()

    flash("Login Succesfull!")
    return redirect(url_for("user"))
  else:
    if "user" in session:
      flash("Already Logged In!")
      return redirect(url_for("user"))

    return render_template('login.html')


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
  if request.method == 'POST':
    email = request.form.get('email')
    firstName = request.form.get('firstName')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    if len(email) < 4:
      flash('Email must be greater than 3 characters.', category='error')
    elif len(firstName) < 2:
      flash('First name must be greater than 1 characters.', category='error')
    elif password1 != password2:
      flash('Passwords don\'t match.', category='error')
    elif len(password1) < 7:
      flash('Password must be atleast 7 characters.', category='error')
    else:
      flash('Account created!', category='success')

  return render_template('sign-up.html')


@app.route("/logout")
def logout():
  if "user" in session:
    user = session["user"]
    flash(f"You have been logged out, {user}", "info")
    session.pop("user", None)

    return redirect(url_for("login"))


# __if __name__ == '__main__':
  # app.run(host='0.0.0.0', debug=True, port=8080)
