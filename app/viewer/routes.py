from app.viewer import bp
from app.authentication import raadzalen, raadzalen_afbeeldingen
from flask import render_template, request, url_for, redirect
from app.functions import get_image_from_id
from firebase_admin import firestore
from app.forms.add import filterForm
from google.cloud.firestore import FieldFilter, Or
@bp.route('/', methods=['POST', 'GET'])
def index():
    rz = raadzalen.order_by("gemeente", direction=firestore.Query.ASCENDING).get()
    rzi = raadzalen_afbeeldingen.get()
    form = filterForm()
    return render_template('viewer/index.html', rz=rz, rzi=rzi, filter_form=filterForm(), rzi_url=get_image_from_id)

@bp.route('/filter', methods=['POST', 'GET'])
def filter():
    opstelling = request.form.get('opstelling')
    college = request.form.get('college')
    spreekgestoelte = request.form.get('spreekgestoelte')
    interrupties = request.form.get('interrupties')
    publiek = request.form.get('publiek')
    publiek_hoogte = request.form.get('publiek_hoogte')
    f_1 = FieldFilter('opstelling', '==', opstelling)
    f_2 = FieldFilter('spreekgestoelte', '==', spreekgestoelte)
    f_3 = FieldFilter('college', '==', college)
    f_4 = FieldFilter('interrupties', '==', interrupties)
    f_5 = FieldFilter('publiek', '==', publiek)
    f_6 = FieldFilter('publiek_hoogte', '==', publiek_hoogte)
    filter_list = []
    if opstelling != '':
        filter_list.append(f_1)

    if spreekgestoelte != '':
        filter_list.append(f_2)

    if college != '':
        filter_list.append(f_3)

    if interrupties != '':
        filter_list.append(f_4)

    if publiek != '':
        filter_list.append(f_5)

    if publiek_hoogte != '':
        filter_list.append(f_6)

    if filter_list.count('') == 0:
        query = raadzalen.order_by("gemeente", direction=firestore.Query.ASCENDING).get()

    elif len(filter_list) > 0:
        or_filter = Or(filters=filter_list)
        query = raadzalen.where(filter=or_filter).get()

    rzi = raadzalen_afbeeldingen.get()
    return render_template('viewer/index.html', rz=query, rzi=rzi, filter_form=filterForm(), rzi_url=get_image_from_id)
