import re

from flask_wtf import FlaskForm
from wtforms import BooleanField, DecimalField, FloatField, IntegerField, \
    DateTimeField, DateField, \
    FileField, PasswordField, StringField, TextAreaField, \
    RadioField, SelectField, SelectMultipleField, \
    HiddenField, SubmitField
from wtforms.validators import Email, InputRequired, Length
from wtforms import ValidationError
#from flask_pagedown.fields import PageDownField
from .models import UserModel


def filter_username(data):
    return re.sub('[^a-z0-9_-]', '', str(data).lower())

def validate_username(self, field):
    if field.data != self.user.keyname and \
            UserModel.query.filter_by(keyname=field.data).first():
        raise ValidationError('Username already in use.')


class CreatUserForm(FlaskForm):
    keyname    = StringField('Username', validators=[InputRequired(),Length(2,63),validate_username], filters=[filter_username])
    submit     = SubmitField('Create User')

    def __init__(self, user, *args, **kwargs):
        super(CreatUserForm, self).__init__(*args, **kwargs)
        #self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user


class EditUserForm(FlaskForm):
    id         = HiddenField('id')
    keyname    = StringField('Username', validators=[InputRequired(),Length(2,63),validate_username], filters=[filter_username])
    active     = BooleanField('Active')
    submit     = SubmitField('Update User')

    def __init__(self, user, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.user = user
