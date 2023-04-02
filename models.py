"""SQLAlchemy models for gymbuddy."""

from flask import Flask
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy() 


class Exercise_of_the_day(db.Model):
  __tablename__ = "exercise_of_the_day"
  id = db.Column(db.Integer, primary_key=True)
  db.ForeignKey('Exercise.id', ondelete="cascade")


class Exercise(db.Model):
  __tablename__ = "exercise"
  id = db.Column(db.Integer, primary_key=True)
  exercise_name = db.Column(db.TEXT)
  exercise_description = db.Column(db.TEXT)
  db.ForeignKey('Exercise_Animation.id', ondelete="cascade")


class Animation(db.Model):
  __tablename__ = "animation"
  id = db.Column(db.Integer, primary_key=True)
  animation_name = db.Column(db.TEXT)
  animation_link = db.Column(db.TEXT)
  db.ForeignKey('Exercise.id', ondelete="cascade"),


class Motivation(db.Model):
  __tablename__ = "motivation"
  id = db.Column(db.Integer, primary_key=True)


class Users(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)

    def __init__(self, name, email, username, password):
        self.name = name
        self.email = email
        self.username = username
        self.password = password

    def __repr__(self):
        """Define representation for User instance."""
        return f"<User id:{self.id} username:{self.username}>"
    
    @classmethod
    def getAll(cls):
        """Return all users"""
        return cls.query.all()

    
    @classmethod
    def signup(cls, name, username, email, password):
        """Sign up user.
        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode("UTF-8")

        user = Users(
            name=name,
            username=username,
            email=email,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.
        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.
        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Notes(db.Model):
  __tablename__ = "notes"

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  text = db.Column(db.String(1000), nullable=False)
  timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
  users_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'),
  nullable=False)

  users = db.relationship("Users")


def connect_db(app):
    """Connect this database to provided Flask app.
    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
   

