from wtforms import StringField, TextAreaField, SubmitField, SelectField, PasswordField, IntegerField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from firebase_admin import auth

c_motieuitspraak = [
    ('We vragen het college om', 'We vragen het college om'),
    ('We geven het college opdracht om', 'We geven het college opdracht om'),
    ('We spreken uit dat', 'We spreken uit dat'),
]
class motieMojo(FlaskForm):
    titel_motie = StringField('Titel van de motie')
    agendapunt_motie = StringField('Agendapunt van de motie')
    constaterende = TextAreaField('Constaterende dat', validators=[DataRequired()])
    overwegende = TextAreaField('Constaterende dat', validators=[DataRequired()])
    uitspraak_titel = SelectField('Opdracht en verzoek', choices=c_motieuitspraak, validators=[DataRequired()])
    uitspraak = TextAreaField('Wat geef je het college mee?', validators=[DataRequired()])
    submit = SubmitField('Genereer motie!')