from flask import render_template, request, redirect, url_for, flash, session
from app.auth.decorators import login_required
from app.motiemojo import bp
from app.authentication import renovaties, raadzalen_afbeeldingen, raadzalen
from app.forms.motie import motieMojo
from datetime import datetime
from google.cloud.firestore import FieldFilter
from docx import Document
from docxtpl import DocxTemplate
@bp.route('/', methods=['POST', 'GET'])
@login_required
def motie():
    form = motieMojo()
    if request.method == 'POST':
        titel_motie = request.form.get('titel_motie')
        agendapunt_motie = request.form.get('agendapunt_motie')
        constaterende = request.form.get('constaterende').splitlines()
        overwegende = request.form.get('overwegende').splitlines()
        uitspraak_titel = request.form.get('uitspraak_titel')
        uitspraak = request.form.get('uitspraak').splitlines()
        template = DocxTemplate('motie_flask_format.docx')
        context = {
            'titel_motie': titel_motie,
            'agendapunt_motie': agendapunt_motie,
            'constaterende': constaterende,
            'overwegingen': overwegende,
            'uitspraak_titel': uitspraak_titel,
            'uitspraak': uitspraak,
            'datum': datetime.now()
        }
        template.render(context)
        template.save('motie_test_heute.docx')
    return render_template('motiemojo/index.html', form=form)
