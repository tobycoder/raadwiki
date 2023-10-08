from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired
class addRenovatie(FlaskForm):
    gemeente = StringField('Gemeente', validators=[DataRequired()])
    architect = StringField('Architect')
    oplever_jaar = IntegerField('Opleverjaar')
    afbeelding = StringField('Impressie')
    afbeelding = StringField('Impressie')
    afbeelding = StringField('Impressie')
    afbeelding = StringField('Impressie')
    grootte = SelectField('Grootte')
    nieuwsberichten = StringField('Nieuwsberichten')
    submit = SubmitField('Verstuur')