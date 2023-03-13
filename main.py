import os
import psycopg2

from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from forms import UserAddForm, LoginForm, MessageForm, EditProfileForm
from models import db, connect_db, User, Notes


CURR_USER_KEY = "curr_user"

###### VIEWS ROUTES


@app.route('/')
def home():
  conn = psycopg2.connect("postgresql://postgres:root@localhost:5432/gymbuddy")
  return 'it works'
  return render_template('index.html')


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


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True, port=8080)
