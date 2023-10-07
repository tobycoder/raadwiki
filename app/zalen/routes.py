from flask import render_template, redirect, url_for, request, flash, session
from app.zalen import bp
from app.authentication import raadzalen, raadzalen_afbeeldingen
from google.cloud.firestore import FieldFilter
from firebase_admin import firestore
from app.forms.add import addPost, addImage, c_opstelling, c_college, c_spreekgestoelte, c_interrupties, c_publiek, c_publiek_positie
from datetime import datetime
import fnmatch
from app.auth.decorators import login_required
@bp.route('/')
@login_required
def index():
    data = raadzalen.order_by("gemeente", direction=firestore.Query.ASCENDING).stream()
    return render_template('zalen/index.html', data=data)

@bp.route('/<id>', methods=['POST', 'GET'])
@login_required
def single_post(id):
    data = raadzalen.document(id).get()
    reference = '/raadzalen/' + str(id)
    foto = raadzalen_afbeeldingen.where('rz_referentie', '==', reference).get()
    return render_template('zalen/single.html', data=data.to_dict(), foto=foto, reference=reference, id=id)

@bp.route('/<id>/edit', methods=['POST', 'GET'])
@login_required
def edit_gegevens(id):
    form_post = addPost()
    form_f = addImage()
    obj = raadzalen.document(id).get()
    obj2 = raadzalen_afbeeldingen.where("rz_referentie", "==", "/raadzalen/" + id).limit(1).get()
    reference = '/raadzalen/' + str(id)
    foto = raadzalen_afbeeldingen.where('rz_referentie', '==', reference).get()
    data2 = raadzalen.document(id).get()
    if request.method == 'POST':
        cap = int(request.form.get('capaciteit'))
        rad = int(request.form.get('raadsleden'))
        if cap and rad != None:
            per = round((cap/rad) * 100, 0)
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
        update = raadzalen.document(id).update(data)
        flash('Je wijzigingen zijn succesvol opgeslagen!')
        return redirect(url_for('zalen.edit_gegevens', id=id))
    return render_template('zalen/edit_2.html', form=form_post, data=data2.to_dict(), form_f=form_f, obj=obj.to_dict(), obj2=obj2, id=id, c_opstelling=c_opstelling, c_college=c_college, c_spreekgestoelte=c_spreekgestoelte, c_interrupties=c_interrupties, c_publiek=c_publiek, c_publiek_positie=c_publiek_positie, foto=foto)

@bp.route('/<id>/edit_afbeelding', methods=['POST', 'GET'])
@login_required
def edit_afbeelding(id):
    form_afbeelding = addImage()
    obj = raadzalen_afbeeldingen.where("rz_referentie", "==", "/raadzalen/" + id).limit(1).get()
    if request.method == 'POST' and len(obj) > 0:
        data = {
            'image_url': request.form.get('afbeelding_url'),
            'rz_referentie': '/raadzalen/' + id
        }
        update = raadzalen_afbeeldingen.document(obj[0].id).update(data)
        flash('Afbeelding succesvol opgeslagen!')
        return redirect(url_for('zalen.edit_gegevens', id=id))
    elif len(obj) == 0 and request.method == 'POST':
        data = {
            'image_url': request.form.get('afbeelding_url'),
            'rz_referentie': '/raadzalen/' + id
        }
        raadzalen_afbeeldingen.add(data)
        return redirect(url_for('zalen.edit_gegevens', id=id))
    else:
        return str(len(obj))
    #return render_template('zalen/edit_image.html', form=form_afbeelding, obj=obj, id=id)

@bp.route('/<id>/delete', methods=['POST', 'GET'])
@login_required
def delete_raadzaal(id):
    delete_gegevens = raadzalen.document(id).delete()
    delete_afbeeldingen = raadzalen_afbeeldingen.where('rz_referentie', '==', '/raadzalen/' + id).get()
    return redirect(url_for('zalen.index'))

