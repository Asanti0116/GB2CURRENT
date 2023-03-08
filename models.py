from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from main import db

db = SQLAlchemy()


class User(db.Model):
  __tablename__ = "user"
  id = db.Column(db.Integer, primary_key=True)
  Name = db.Column(db.text, nullable=False)
  Username = db.Column(db.text, nullable=False, unique=True)
  Password = db.Column(db.text, nullable=False)
  Email = db.Column(db.text, nullable=False)


class Exercise_of_the_day(db.Model):
  __tablename__ = "exercise_of_the_day"
  id = db.Column(db.Integer, primary_key=True)
  exercise_id = db.Column(db.Integer)


class Exercise(db.Model):
  __tablename__ = "exercise"
  id = db.Column(db.Integer, primary_key=True)
  exercise_name = db.Column(db.TEXT)
  exercise_description = db.Column(db.TEXT)
  exercise_animation_id = db.Column(db.Integer)


class Animation(db.Model):
  __tablename__ = "animation"
  id = db.Column(db.Integer, primary_key=True)
  animation_name = db.Column(db.TEXT)
  animation_link = db.Column(db.TEXT)


class Motivation(db.Model):
  __tablename__ = "motivation"
  id = db.Column(db.Integer, primary_key=True)


class Notes(db.Model):
  __tablename__ = "notes"
  id = db.Column(db.Integer, primary_key=True)
  Title = db.Column(db.String(100))
  Note_text = db.Column(db.String(5000))C
  Created = db.Column(db.DateTime, default=datetime.now())
