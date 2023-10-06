from app.add import bp
from app.forms.add import addPost, addImage, c_opstelling, c_college, c_spreekgestoelte, c_interrupties, c_publiek_positie, c_publiek
from flask import request, redirect, url_for, render_template
from app.authentication import raadzalen, raadzalen_afbeeldingen
from datetime import datetime

@bp.route('/', methods=['POST', 'GET'])
def index():
    form_post = addPost()
    if request.method == 'POST':
        cap = request.form.get('capaciteit')
        rad = request.form.get('raadsleden')
        if cap and rad:
            per = round((cap / rad) * 100, 0)
        else:
            per = 0
        data = {
            'gemeente': request.form.get('gemeente'),
            'raadsleden': request.form.get('raadsleden'),
            'bg': request.form.get('burgemeester'),
            'bg_update': datetime.utcnow(),
            'updated': datetime.utcnow(),
            'opstelling': request.form.get('opstelling'),
            'college': request.form.get('college'),
            'spreekgestoelte': request.form.get('spreekgestoelte'),
            'interrupties': request.form.get('interrupties'),
            'publiek': request.form.get('publiek'),
            'publiek_positie': request.form.get('publiek_positie'),
            'capaciteit': request.form.get('capaciteit'),
            'capaciteit_percentage': per
        }
        obj = raadzalen.add(data)
        rz_id = obj[1].id
        return redirect(url_for('zalen.edit_gegevens', id=rz_id))
    return render_template('add/gegevens.html', form=form_post)

@bp.route('/<id>/afbeelding', methods=['POST', 'GET'])
def add_image(id):
    form_image = addImage()
    if request.method == 'POST':
        data = {
            'image_url': request.form.get('afbeelding_url'),
            'rz_referentie': '/raadzalen/' + id
        }
        raadzalen_afbeeldingen.add(data)
        return redirect(url_for('zalen.index'))
    return render_template('add/afbeelding.html', form=form_image, id=id)

# SELECT OPTIONS