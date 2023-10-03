from wtforms import StringField, TextAreaField, SubmitField, SelectField, PasswordField, IntegerField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

class addPost(FlaskForm):
    gemeente = StringField('Gemeente', validators=[DataRequired()])
    burgemeester = StringField('Burgemeester', validators=[DataRequired()])
    raadsleden = IntegerField('Aantal raadsleden', validators=[DataRequired()])
    submit = SubmitField('Submit')

class addImage(FlaskForm):
    afbeelding_url = StringField('Afbeelding van de raadzaal', validators=[DataRequired()])
    submit = SubmitField('Voeg toe')