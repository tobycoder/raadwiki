from app.dashboard import bp
from flask import render_template, url_for, request, redirect, session
from app.auth.decorators import login_required
from app.authentication import raadzalen, renovaties
from firebase_admin import firestore
from google.cloud.firestore import FieldFilter
from app.functions import count_entries, count_raadzalen_by_user, count_renovaties_by_user
@bp.route('/', methods=['POST', 'GET'])
@login_required
def index():
    rz = raadzalen.order_by("updated", direction=firestore.Query.DESCENDING).limit(5).stream()
    ren = renovaties.order_by("laatste_update", direction=firestore.Query.DESCENDING).limit(5).stream()
    pRen = renovaties.where(filter=FieldFilter('auteur', '==', session['user'])).limit(5).get()
    pRz = raadzalen.where(filter=FieldFilter('auteur', '==', session['user'])).limit(5).get()
    cRen = count_entries(renovaties)
    cRz = count_entries(raadzalen)
    pcRz = count_raadzalen_by_user(session["user"])
    pcRen = count_renovaties_by_user(session["user"])
    return render_template('dashboard/index.html', rz=rz, ren=ren, pRen=pRen, pRz=pRz, cRen=cRen, cRz=cRz, pcRz=pcRz, pcRen=pcRen)

