import os

from app.auth import bp
from firebase_admin.auth import UserRecord
from app.authentication import fb
from firebase_admin import auth
from app.forms.login import registerForm, loginForm, approvalForm
from flask import render_template, request, url_for, redirect, flash, session
from flask_mail import Mail, Message
import requests
import json
from app import mail
import os
from app.auth.decorators import master_required, login_required

FIREBASE_WEB_API_KEY = os.environ.get('FIREBASE_WEB_API_KEY')
rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
master_email = os.environ.get('MAIL_USERNAME')
send_master = os.environ.get('MASTER_EMAIL')
@bp.route('/register', methods=['POST', 'GET'])
def rw_create_user():
    form = registerForm()
    if request.method == 'POST':
        display_name = request.form.get('display_name')
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.create_user(email=email, password=password, display_name=display_name, disabled=True)
            msg = Message(subject='We gaan je registratie bekijken', sender=master_email, recipients=[email])
            msg.body = "Alvast van harte welkom " + display_name + " en leuk dat je mee wil helpen! Een beheerder gaat je aanvraag zometeen goedkeuren. Je ontvangt dan nader bericht."
            mail.send(msg)
            msg_2 = Message(subject='Nieuwe registratie', sender=master_email,
                          recipients=[send_master])
            msg_2.html = "<h1>Er is een nieuwe registratie. Graag goedkeuren.</h1><a href='http://127.0.0.1:5000/auth/{a}/approval'>Keur hier lokaal goed</a><a href='http://borisdefloer.pythonanywhere.com/auth/{a}/approval'>Keur hier online goed</a>".format(a=user.uid)
            mail.send(msg_2)
            return render_template('auth/approval.html')
        except:
            flash('Oei, probeer opnieuw met een andere email. Deze bestaat al.')
            return render_template('auth/register.html', form=form)
    else:
        return render_template('auth/register.html', form=form)

@bp.route('/login', methods=['POST', 'GET'])
def rw_login_user():
    form = loginForm()
    if 'user' in session:
        return redirect(url_for('dashboard.index'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        payload = json.dumps({
            "email": email,
            "password": password,
            "returnSecureToken": True
        })

        r = requests.post(rest_api_url,
                          params={"key": FIREBASE_WEB_API_KEY},
                          data=payload)
        callback = r.json()
        if "error" in callback:
            flash("Je hebt waarschijnlijk verkeerde gegevens ingevuld. Probeer opnieuw.")
            return render_template('auth/login.html', form=form)
        else:
            flash('Welkom, ' + email)
            session['user'] = email
            return redirect(url_for('dashboard.index'))

    return render_template('auth/login.html', form=form)

@bp.route('/logout')
def logout():
    if('user' in session):
        session.pop('user')
        return redirect(url_for('auth.rw_login_user'))
    else:
        return redirect(url_for('auth.rw_login_user'))

@bp.route('/<u_id>/approval', methods=['POST', 'GET'])
@login_required
@master_required
def approval(u_id):
    form = approvalForm()
    user = auth.get_user(u_id)
    display_name = user.display_name
    user_email = user.email
    meta = user.disabled
    if user.disabled == False:
        return render_template('auth/master_approval.html', u_id=u_id, form=form, display_name=display_name, user_email=user_email, meta=meta, message="Deze gebruiker is al goedgekeurd.")
    if request.method == 'POST':
        approved = auth.update_user(u_id, disabled=False)
        email = user.email
        msg = Message(subject='Je account is goedgekeurd door een beheerder.', sender=master_email, recipients=[email])
        msg.body = "Je kan nu inloggen. Veel succes en bedankt voor de hulp!"
        mail.send(msg)
        return redirect(url_for('dashboard.index'))
    return render_template('auth/master_approval.html', u_id=u_id, form=form, display_name=display_name, user_email=user_email, meta=meta,)


