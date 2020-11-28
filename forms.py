from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, NumberRange, Email


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign up')


class CreateTripForm(FlaskForm):
    source = StringField('From',
                         validators=[DataRequired(), Length(min=2, max=20)])
    destination = StringField(
        'To', validators=[DataRequired(), Length(min=2, max=20)])
    budget = IntegerField('Your budget', validators=[
                         DataRequired(), NumberRange(min=0, max=999999)])
    submit = SubmitField('Create new')
