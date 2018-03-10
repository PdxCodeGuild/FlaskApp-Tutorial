import re

from flask_wtf import FlaskForm
from wtforms import BooleanField, DecimalField, FloatField, IntegerField, \
    DateTimeField, DateField, \
    FileField, PasswordField, StringField, TextAreaField, \
    RadioField, SelectField, SelectMultipleField, \
    HiddenField, SubmitField
from wtforms.validators import InputRequired, Length
from wtforms import ValidationError
from .models import ItemModel


def filter_keyname(data):
    return re.sub('[^a-z0-9_-]', '', str(data).lower())

def validate_keyname(self, field):
    if field.data != self.item.keyname and \
            ItemModel.query.filter_by(keyname=field.data).first():
        raise ValidationError('Keyname already in use.')


class CreatItemForm(FlaskForm):
    keyname    = StringField('Keyname', validators=[InputRequired(),Length(2,63),validate_keyname], filters=[filter_keyname])
    submit     = SubmitField('Create Item')

    def __init__(self, item, *args, **kwargs):
        super(CreatItemForm, self).__init__(*args, **kwargs)
        self.item = item


class EditItemForm(FlaskForm):
    id         = HiddenField('id')
    keyname    = StringField('Keyname', validators=[InputRequired(),Length(2,63),validate_keyname], filters=[filter_keyname])
    mod_create = DateTimeField('Item Created')
    submit     = SubmitField('Update Item')

    def __init__(self, item, *args, **kwargs):
        super(EditItemForm, self).__init__(*args, **kwargs)
        self.item = item

