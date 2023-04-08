import os


from flask import Flask, redirect, url_for, render_template, request, session, flash, g, jsonify
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from forms import UserAddForm, LoginForm, NotesForm
from models import db, connect_db, Users, Notes
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate

CURR_USER_KEY = "curr_user"
# API_BASE_URL = 

app = Flask(__name__)

import requests
import json

url = "https://exercisedb.p.rapidapi.com/exercises"

headers = {
	"X-RapidAPI-Key": "9ded74f4f8msha4284305d05698dp19f784jsn6e8a645eabe3",
	"X-RapidAPI-Host": "exercisedb.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers)

# print(response.text)
print(response.json())





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


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.filter(Users.id == int(user_id)).first()

@login_manager.unauthorized_handler
def unauthorized():
    flash('Please login first.', 'danger')
    
    return redirect(url_for('login'))

login_manager.login_view = 'login'



##############################################################################

# @app.before_request
# def add_user_to_g():
    # """If we're logged in, add curr user to Flask global."""

    # if CURR_USER_KEY in session:
        # g.user = Users.query.get(session[CURR_USER_KEY])

    # else:
        # g.user = None


# def login_user(user):
    # """Log in user."""

    # session[CURR_USER_KEY] = user.id


# def logout_user():
    # """Logout user."""

    # if CURR_USER_KEY in session:
        # del session[CURR_USER_KEY]


#############################################################################

@app.route('/', methods=['GET'])
def landing():
    """Show homepage."""
    return render_template('home-anon.html')


######## User routes #########################################################

@app.route('/sign-up', methods=["GET", "POST"])
def signup():
    """Handle user signup.
    Create new user and add to DB. Redirect to home page.
    If form not valid, present form.
    If there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    try:
        if form.validate_on_submit():
            user = Users.signup(
                name=form.name.data,
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
              )
            
            db.session.commit()

            login_user(user)
            
            flash('Successfully created your account!','success')

            return render_template('/logged-in.html')

    except IntegrityError as err:
        err_info = jsonify(err.orig.args[0]).get_json()
        
        if "users_username_key" in err_info:
            flash('Username already taken.', 'danger')
        if "users_email_key" in err_info:
            flash('Email already taken.', 'danger')
    
    return render_template('sign-up.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login, add to session."""

    form = LoginForm()

    if form.validate_on_submit():
        user = Users.authenticate(form.username.data,
                                 form.password.data)

        if user:
            login_user(user, remember=True)
            flash(f"Hello, {Users.username}!", "info")

            return redirect("/logged-in")
        
        flash("Invalid credentials.", 'danger')

    return render_template('/login.html', form=form)
        
@app.route('/logged-in', methods=['GET'])
def loggedin():
    """Show homepage for logged in users."""
    return render_template('logged-in.html')


@app.route('/logout')
def logout():
    """Handle logout of user, remove from session."""

    # Logs out user - PS
    logout_user()

    flash("Logged Out", 'info')

    return render_template('home-anon.html')



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
