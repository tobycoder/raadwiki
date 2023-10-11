from wtforms import StringField, TextAreaField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from flask_wtf.file import FileField

class registerForm(FlaskForm):
    display_name = StringField('Voornaam', validators=[DataRequired()])
    avatar = FileField('Profielfoto', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class loginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class approvalForm(FlaskForm):
    submit = SubmitField('Keur goed!')


class passwordReset(FlaskForm):
    password = PasswordField('Nieuwe wachtwoord')
    password_repeat = PasswordField('Herhaal')
    submit = SubmitField('Wijzig wachtwoord')

class replyForm(FlaskForm):
    content = TextAreaField('Reply', validators=[DataRequired()])
    submit = SubmitField('Verstuur')