from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField, FloatField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, NumberRange, Email


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=50)])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign up')


class CreateTripForm(FlaskForm):
    source = StringField('From',
                         validators=[DataRequired(), Length(min=2, max=60)])
    destination = StringField(
        'To', validators=[DataRequired(), Length(min=2, max=60)])
    budget = FloatField('Your budget', validators=[
                         DataRequired(), NumberRange(min=0, max=999999)])
    submit = SubmitField('Create new')


class CreateTeamMemberForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=50)])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    budget = IntegerField('Budget', validators=[
                         DataRequired(), NumberRange(min=0, max=999999)])
    submit = SubmitField('Submit')


class AddNewExpenseForm(FlaskForm):
    sum = FloatField('Enter sum', validators=[
                      DataRequired(), NumberRange(min=0, max=999999)])
    category = StringField('Category', validators=[
                            DataRequired(), Length(min=2, max=50)])
    notes = StringField('Place for your notes..')
    submit = SubmitField('Done')
