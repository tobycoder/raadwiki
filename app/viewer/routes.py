from app.viewer import bp
from app.authentication import raadzalen, raadzalen_afbeeldingen
from flask import render_template, request, url_for, redirect
from app.functions import get_image_from_id
from firebase_admin import firestore
@bp.route('/')
def index():
    rz = raadzalen.order_by("gemeente", direction=firestore.Query.ASCENDING).get()
    rzi = raadzalen_afbeeldingen.get()
    return render_template('viewer/index.html', rz=rz, rzi=rzi, rzi_url=get_image_from_id)
