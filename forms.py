from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Optional, NumberRange, DataRequired


class NotesForm(FlaskForm):
    """Form for adding/editing notes."""

    text = TextAreaField('text', validators=[DataRequired()])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    name = StringField('name', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    email = StringField("email", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])
    


class LoginForm(FlaskForm):
    """Form for user login."""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])