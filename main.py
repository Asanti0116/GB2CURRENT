import os
import requests

from flask import Flask, redirect, url_for, render_template, request, session, flash, g, jsonify
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from forms import UserAddForm, LoginForm, NotesForm
from models import db, connect_db, Users, Notes
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate

from forms import UserAddForm, LoginForm, NotesForm
from models import db, connect_db, Users, Notes

CURR_USER_KEY = "curr_user"


app = Flask(__name__)

# code block for workouts tab ---------------------------------------------------
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

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:Pickles1011!@localhost:5433/gym_buddy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
migrate = Migrate(app, db)
app.config['SECRET_KEY'] = "shhh-dont-tell-anyone"


connect_db(app)
app.app_context().push()
db.create_all() # <--- create db object.


#login_manager = LoginManager()
#login_manager.init_app(app)
#
#@login_manager.user_loader
#def load_user(user_id):
#    return Users.query.get(int(user_id))
#
#@login_manager.unauthorized_handler
#def unauthorized():
#    flash('Please login first.', 'danger')
#    
#    return redirect(url_for('login'))
#
#login_manager.login_view = 'login'



##############################################################################

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
        session.clear()




#############################################################################

#@app.route('/', methods=['GET', 'POST'])
#def landing():
#    """Show homepage."""
#    return render_template('home-anon.html')
#
@app.route('/')
def home():
    """Show homepage:
    - index.html: not logged in
    -redirect to user's page that shows all links : logged in"""

    if g.user:
    
        return redirect(f"/users/{g.user.id}")
    
    return render_template('index.html')





@ app.route('/about')
def about():
    """render about page"""
    return render_template('about.html')


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

    if form.validate_on_submit():
        try:
            user = Users.signup(
                name=form.name.data,
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
            )
            
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('/sign-up.html', form=form)

        do_login(user)

        return render_template('home-anon.html')

    else:
        return render_template('/sign-up.html', form=form)
       
 
@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login, add to session."""

    form = LoginForm()

    if form.validate_on_submit():
        user = Users.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {Users.username}!", "success")
            return redirect("/dashboard")
        
        flash("Invalid credentials.", 'danger')

    return render_template('/login.html', form=form)
        
@app.route('/dashboard', methods=['GET'])
def dashboard():
    """Show homepage for logged in users."""
    return render_template('dashboard.html')


@app.route('/logout')
def log_out():

    do_logout()

    flash("See you later!", "success")
    return redirect('/')
    



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
