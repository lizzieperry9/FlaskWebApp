import re
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required, Email, Length, EqualTo, ValidationError


# Checks that no the data contains none of the characters below
def character_check(form, field):
    excluded_chars = "* ? ! ' ^ + % & / ( ) = } ] [ { $ # @ < >"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(
                f"Character {char} is not allowed.")


# Checks phone data is in correct format XXXX-XXX-XXXX
def phone_check(form, field):
    t = re.compile(r'^\d\d\d\d-\d\d\d-\d\d\d\d$')
    if not t.match(field.data):
        raise ValidationError("Phone must be of the form XXXX-XXX-XXXX")


# Register form class
class RegisterForm(FlaskForm):
    email = StringField(validators=[Required(), Email()])
    firstname = StringField(validators=[Required(), character_check])
    lastname = StringField(validators=[Required(), character_check])
    phone = StringField(validators=[Required(), phone_check])
    password = PasswordField(validators=[Required(), Length(min=6, max=12, message='Password must be between 6 and 12 '
                                                                                   'characters in length.')])
    confirm_password = PasswordField(validators=[Required(), EqualTo('password', message='Both password fields must '
                                                                                         'be equal!')])
    pin_key = StringField(validators=[Required(), Length(min=32, max=32, message='PIN Key must be 32 characters in '
                                                                                 'length.')])
    submit = SubmitField()


# Checks password meets password policy
def validate_password(self, password):
    p = re.compile(r'(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*\W)')
    if not p.match(self.password.data):
        raise ValidationError("Password must contain at least 1 digit, 1 lowercase letter 1 uppercase letter and "
                              "1 special character.")


# Login Form
class LoginForm(FlaskForm):
    email = StringField(validators=[Required(), Email()])
    password = PasswordField(validators=[Required()])
    pin = StringField(validators=[Required()])
    submit = SubmitField()
