import os


from flask import Flask, redirect, url_for, render_template, request, session, flash, g, jsonify
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from forms import UserAddForm, LoginForm, NotesForm
from models import db, connect_db, Users, Notes
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate

app = Flask(__name__)


CURR_USER_KEY = "curr_user"


# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:Pickles1011!@localhost:5432/gym_buddy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
migrate = Migrate(app, db)
app.config['SECRET_KEY'] = "shhh-dont-tell-anyone"
connect_db(app)
app.app_context().push()
db.create_all() # <--- create db object.



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

    session[CURR_USER_KEY] = Users.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

# *********************************************************************** #
# Homepage and Handling Signup/Login/Logout

@app.route('/')
def home():
  return render_template('index.html', Users=g.user)


@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
    """Shows signup page and handles form submission."""

    form = UserAddForm()

    if form.validate_on_submit():
        try:

            Users = Users.signup(
                username=form.username.data,
                name=form.name.data,
                email=form.email.data,
                password=form.password.data)
            db.session.commit()

        except IntegrityError:
            flash("Username already taken. Please try another.", 'danger')
            return render_template('sign-up.html', form=form)

        do_login(Users)

        return redirect('/')

    else:
        return render_template('sign-up.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        Users = Users.authenticate(
            form.username.data, form.password.data)

        if Users:
            do_login(Users)
            flash(f"Hello, {Users.username}!", 'success')
            return redirect('/')

        flash("Invalid credentials. Please try again if you have already signed up. Otherwise please click the signup button to join.", 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Handle user logout."""
    do_logout()
    flash("You have been logged out. Log back in below to access all of the features.", 'success')
    return redirect('/login')





# *********************************************************************** #





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








if __name__ == '__main__':
    
    app.run(debug=True)

#if above doesn't work, delete and reinstate whats below
# __if __name__ == '__main__':
  # app.run(host='0.0.0.0', debug=True, port=8080)
