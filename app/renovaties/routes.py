from flask import render_template, request, redirect, url_for, flash
from app.auth.decorators import login_required
from app.renovaties import bp
from app.authentication import renovaties, raadzalen_afbeeldingen, raadzalen
from app.forms.renovaties import addRenovatie
from datetime import datetime
choices = [
    ('Klein', 'Klein'),
    ('Gehele raadzaal', 'Gehele raadzaal'),
    ('Gehele gemeentehuis', 'Gehele Gemeentehuis'),
]

@bp.route('/')
def index():
    query = renovaties.get()
    return render_template('renovaties/index.html', data=query)

@bp.route('/add', methods=['POST', 'GET'])
def add():
    form = addRenovatie()
    if request.method == 'POST':
        data = {
            'gemeente': request.form.get('gemeente'),
            'architect': request.form.get('architect'),
            'oplever_jaar': request.form.get('oplever_jaar'),
            'grootte': request.form.get('grootte'),
            'nieuwsberichten': [request.form.get('nieuwsberichten')],
            'afbeeldingen': request.form.getlist('afbeelding'),
            'laatste_update': datetime.utcnow()
        }
        new = renovaties.add(data)
        flash('Gelukt, voeg nu de rest van de gegevens toe.')
        return redirect(url_for('renovaties.edit', id=new[1].id))
    return render_template('renovaties/add.html', form=form, choices=choices)

@bp.route('/<id>/edit', methods=['POST', 'GET'])
def edit(id):
    form = addRenovatie()
    query = renovaties.document(id).get()
    if request.method == 'POST':
        data = {
            'gemeente': request.form.get('gemeente'),
            'architect': request.form.get('architect'),
            'oplever_jaar': request.form.get('oplever_jaar'),
            'grootte': request.form.get('grootte'),
            'nieuwsberichten': [request.form.get('nieuwsberichten')],
            'afbeeldingen': request.form.getlist('afbeelding'),
            'laatste_update': datetime.utcnow()
        }
        try:
            renovaties.document(id).update(data)
            return redirect(url_for('renovaties.edit', id=id))
        except:
            flash('Er ging iets mis. Probeer opnieuw.')
            return render_template('renovaties/edit.html', id=id, data=query.to_dict(), form=form, choices=choices)
    return render_template('renovaties/edit.html', id=id, data=query.to_dict(), form=form, choices=choices)


@bp.route('/<id>/delete')
def delete(id):
    renovaties.document(id).delete()
    return redirect(url_for('renovaties.index'))