from wtforms import StringField, TextAreaField, SubmitField, SelectField, PasswordField, IntegerField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

c_opstelling = [
    ('', ''),
    ('Klassikaal', 'Klassikaal'),
    ('Lagerhuis', 'Lagerhuis'),
    ('Hoefijzer', 'Hoefijzer'),
    ('Theater', 'Theater'),
    ('Cirkel', 'Cirkel'),
    ('Onbekend', 'Onbekend')
]

c_college = [
    ('', ''),
    ('Monistisch', 'Monistisch'),
    ('Dualistisch', 'Dualistisch'),
    ('Extraparlementair', 'Extraparlementair'),
    ('Tribunaal', 'Tribunaal'),
    ('Onbekend', 'Onbekend')
]

c_spreekgestoelte = [
    ('', ''),
    ('Ja', 'Ja'),
    ('Nee', 'Nee'),
    ('Onbekend', 'Onbekend')
]

c_interrupties = [
    ('', ''),
    ('Eigen plaats', 'Eigen plaats'),
    ('Interruptiemicrofoons', 'Interruptiemicrofoons'),
    ('Onbekend', 'Onbekend')
]

c_publiek = [
    ('', ''),
    ('Achter de voorzitter', 'Achter de voorzitter'),
    ('Achter de raadsleden', 'Achter de raadsleden'),
    ('Achter de raadsleden en voorzitter', 'Achter de raadsleden en voorzitter'),
    ('Onbekend', 'Onbekend')
]

c_publiek_positie = [
    ('', ''),
    ('Gelijkvloers', 'Gelijkvloers'),
    ('Verhoogd', 'Verhoogd'),
    ('Contact mogelijk', 'Contact mogelijk')
]
class addPost(FlaskForm):
    gemeente = StringField('Gemeente', validators=[DataRequired()])
    burgemeester = StringField('Burgemeester', validators=[DataRequired()])
    raadsleden = IntegerField('Aantal raadsleden', validators=[DataRequired()])
    opstelling = SelectField('Opstelling', choices=c_opstelling, validators=[DataRequired()])
    college = SelectField('Plaats college', choices=c_college, validators=[DataRequired()])
    spreekgestoelte = SelectField('Spreekgestoelte', choices=c_spreekgestoelte, validators=[DataRequired()])
    interrupties = SelectField('Interrupties', choices=c_interrupties, validators=[DataRequired()])
    publiek = SelectField('Publieke ruimte', choices=c_publiek ,validators=[DataRequired()])
    publiek_positie = SelectField('Hoogte publiek', choices=c_publiek_positie, validators=[DataRequired()])
    capaciteit = IntegerField('Capaciteit', validators=[DataRequired()])
    submit = SubmitField('Submit')

class addImage(FlaskForm):
    afbeelding_url = StringField('Afbeelding van de raadzaal', validators=[DataRequired()])
    submit = SubmitField('Voeg toe')

class filterForm(FlaskForm):
    opstelling = SelectField('Opstelling', choices=c_opstelling)
    college = SelectField('Plaats college', choices=c_college)
    spreekgestoelte = SelectField('Spreekgestoelte', choices=c_spreekgestoelte)
    interrupties = SelectField('Interrupties', choices=c_interrupties)
    publiek = SelectField('Publieke ruimte', choices=c_publiek)
    publiek_positie = SelectField('Hoogte publiek', choices=c_publiek_positie)
    submit = SubmitField('Filter')
