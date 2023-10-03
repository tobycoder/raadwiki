from flask import render_template, redirect, url_for, request
from app.zalen import bp
from app.authentication import raadzalen, raadzalen_afbeeldingen
from google.cloud.firestore import FieldFilter
from firebase_admin import firestore
from app.forms.add import addPost, addImage
from datetime import datetime

@bp.route('/')
def index():
    data = raadzalen.order_by("gemeente", direction=firestore.Query.ASCENDING).stream()
    return render_template('zalen/index.html', data=data)

@bp.route('/<id>', methods=['POST', 'GET'])
def single_post(id):
    data = raadzalen.document(id).get()
    reference = '/raadzalen/' + str(id)
    foto = raadzalen_afbeeldingen.where('rz_referentie', '==', reference).get()
    return render_template('zalen/single.html', data=data.to_dict(), foto=foto, reference=reference, id=id)

@bp.route('/<id>/edit', methods=['POST', 'GET'])
def edit_gegevens(id):
    form_post = addPost()
    obj = raadzalen.document(id).get()
    if request.method == 'POST':
        data = {
            'gemeente': request.form.get('gemeente'),
            'raadsleden': request.form.get('raadsleden'),
            'bg': request.form.get('burgemeester'),
            'bg_update': datetime.utcnow(),
            'updated': datetime.utcnow()
        }
        update = raadzalen.document(id).update(data)
        return redirect(url_for('zalen.edit_afbeelding', id=id))
    return render_template('zalen/edit.html', form=form_post, obj=obj.to_dict(), id=id)

@bp.route('/<id>/edit_afbeelding', methods=['POST', 'GET'])
def edit_afbeelding(id):
    form_afbeelding = addImage()
    obj = raadzalen_afbeeldingen.where("rz_referentie", "==", "/raadzalen/" + id).limit(1).get()
    if request.method == 'POST':
        data = {
            'image_url': request.form.get('afbeelding_url'),
            'rz_referentie': '/raadzalen/' + id
        }
        update = raadzalen_afbeeldingen.document(obj[0].id).update(data)
        return redirect(url_for('zalen.index'))
    return render_template('zalen/edit_image.html', form=form_afbeelding, obj=obj, id=id)

@bp.route('/<id>/delete', methods=['POST', 'GET'])
def delete_raadzaal(id):
    delete_gegevens = raadzalen.document(id).delete()
    delete_afbeeldingen = raadzalen_afbeeldingen.where('rz_referentie', '==', '/raadzalen/' + id).get()
    return redirect(url_for('zalen.index'))

