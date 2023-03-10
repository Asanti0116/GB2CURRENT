from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional


class NotesForm(FlaskForm):
    """Form for adding/editing notes."""

    text = TextAreaField('text', validators=[DataRequired()])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    


class LoginForm(FlaskForm):
    """Login form."""

    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])