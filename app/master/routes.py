import os

from app.master import bp
from flask import render_template, request, redirect, url_for, flash, session
from app.auth.decorators import master_required, login_required
from firebase_admin import auth
from app.forms.login import registerForm
from flask_mail import Message
from app import mail
from app.functions import count_raadzalen_by_user, count_renovaties_by_user
from app.authentication import messages, raadzalen, renovaties
from firebase_admin import firestore

send_master = os.environ.get('MAIL_USERNAME')
master_email = os.environ.get('MASTER_EMAIL')
@bp.route('/')
@master_required
@login_required
def index():
    page = auth.list_users()
    return render_template('master/index.html', auth=auth, count_raadzalen_by_user=count_raadzalen_by_user, count_renovaties_by_user=count_renovaties_by_user)

@bp.route('/add', methods=['POST', 'GET'])
@master_required
@login_required
def add():
    form = registerForm()
    if request.method == 'POST':
        display_name = request.form.get('display_name')
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.create_user(email=email, password=password, display_name=display_name, disabled=False)
            msg = Message(subject='Welkom bij raadwiki!', sender=master_email, recipients=[email])
            msg.body = "Welkom " + display_name + " en leuk dat je mee wil helpen! " + session['user'] + " heeft je account aangemaakt. Je kan inloggen met de door hem verstrekte inloggegevens."
            mail.send(msg)
            return redirect(url_for('master.index'))
        except:
            flash('Oei, probeer opnieuw met een andere email. Deze bestaat al.')
            return render_template('master/create_user.html', form=form)
    else:
        return render_template('master/create_user.html', form=form)
@bp.route('/<id>/approve')
@master_required
@login_required
def approve(id):
    user = auth.get_user(id)
    if user.disabled == False:
        update = auth.update_user(id, disabled=True)
        email = user.email
        msg = Message(subject='Je account is uitgeschakeld door een beheerder.', sender=master_email, recipients=[email])
        msg.body = "Een beheerder heeft je account uitgeschakeld. Neem contact op voor meer informatie."
        mail.send(msg)
    elif user.disabled == True:
        update = auth.update_user(id, disabled=False)
        email = user.email
        msg = Message(subject='Je account is goedgekeurd door een beheerder.', sender=master_email, recipients=[email])
        msg.body = "Je kan nu inloggen. Veel succes en bedankt voor de hulp!"
        mail.send(msg)
    else:
        return redirect(url_for('master.index'))
    return redirect(url_for('master.index'))


@bp.route('/bericht-naar-allen')
@master_required
@login_required
def bericht_naar_allen():

    if request.method == 'POST':
        data = {
            'from': session['user'],
            'to': 'notification',
            'content': request.form.get('content'),
            'subject': request.form.get('subject'),
        }
        messages.add(data)
@bp.route('/<id>/delete')
@master_required
@login_required
def delete(id):
    delete = auth.delete_user(id)
    return redirect(url_for('master.index'))

@bp.route('/workload')
@master_required
@login_required
def workload():
    data = raadzalen.order_by("gemeente", direction=firestore.Query.ASCENDING).stream()
    return render_template('master/workload.html', data=data)
