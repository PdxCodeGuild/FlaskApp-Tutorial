import re

from flask_wtf import FlaskForm
from wtforms import BooleanField, DecimalField, FloatField, IntegerField, \
    DateTimeField, DateField, \
    FileField, PasswordField, StringField, TextAreaField, \
    RadioField, SelectField, SelectMultipleField, \
    HiddenField, SubmitField
from wtforms.validators import Email, EqualTo, InputRequired, Length
from wtforms import ValidationError
#from flask_pagedown.fields import PageDownField
from .models import UserModel


def filter_username(data):
    return re.sub('[^a-z0-9_-]', '', str(data).lower())

def filter_useremail(data):
    return str(data).lower()

def validate_username(self, field):
    if field.data != self.user.keyname and \
            UserModel.query.filter_by(keyname=field.data).first():
        raise ValidationError('Username already in use.')

def validate_usermail(self, field):
    if field.data != self.user.user_email and \
            UserModel.query.filter_by(user_email=field.data).first():
        raise ValidationError('Email address already in use.')


class LoginForm(FlaskForm):
    next       = HiddenField('next')
    user_email = StringField('Email', validators=[InputRequired(),Length(1,255),Email()])
    password   = PasswordField('Password', validators=[InputRequired()])
    remember   = BooleanField('Keep me logged in')
    submit     = SubmitField('Login')

    def __init__(self, user, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = user


class CreatUserForm(FlaskForm):
    keyname    = StringField('Username', validators=[InputRequired(),Length(2,63),validate_username], filters=[filter_username])
    user_email = StringField('Email', validators=[InputRequired(),Length(1,63),Email(),validate_usermail], filters=[filter_useremail])
    password   = PasswordField('Password', validators=[InputRequired(),Length(1,31),EqualTo('password2',message="Passwords must match.")])
    password2  = PasswordField('Confirm Password')
    submit     = SubmitField('Create User')

    def __init__(self, user, *args, **kwargs):
        super(CreatUserForm, self).__init__(*args, **kwargs)
        self.user = user


class EditUserForm(FlaskForm):
    id         = HiddenField('id')
    active     = BooleanField('Active')
    keyname    = StringField('Username', validators=[InputRequired(),Length(2,63),validate_username], filters=[filter_username])
    user_email = StringField('Email', validators=[InputRequired(),Length(1,63),Email(),validate_usermail], filters=[filter_useremail])
    password   = PasswordField('Password', validators=[EqualTo('password2',message="Passwords must match.")])
    password2  = PasswordField('Confirm Password')
    submit     = SubmitField('Update User')

    def __init__(self, user, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.user = user
