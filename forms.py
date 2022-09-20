from configparser import LegacyInterpolation
from tarfile import LENGTH_LINK
from flask_wtf import FlaskForm
import email
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo

# from app import User


class RegistrationForm(FlaskForm):
    username = StringField('Name : ', validators=[DataRequired()])
    email = EmailField('Email : ', validators=[DataRequired(), Email()])
    # check how to use a TelField in flask
    phone = StringField('Phone Number : ', validators=[DataRequired(), Length(min=11, max=15)])
    password = PasswordField('Password ', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # def validate_email(self, field):
    #     if User.query.filter_by(email=field.data).first():
    #         raise ValidationError('Email already in use')

class LoginForm(FlaskForm):
    email = EmailField('Enter email : ', validators=[DataRequired(), Email()])
    password = PasswordField('Password : ', validators=[DataRequired(), Length(min=8)])
    remember_me = BooleanField('Remember me.')
    login = SubmitField('Login')