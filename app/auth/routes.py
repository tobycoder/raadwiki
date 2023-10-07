from app.auth import bp
from firebase_admin.auth import UserRecord
from app.authentication import fb
from firebase_admin import auth
from app.forms.login import registerForm, loginForm
from flask import render_template, request, url_for, redirect, flash, session
from flask_mail import Mail, Message
import requests
import json
from app import mail

FIREBASE_WEB_API_KEY = "AIzaSyAE9eQ9xTvwIIAohWLMkLl--YR89VshWsg"
rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

@bp.route('/register', methods=['POST', 'GET'])
def rw_create_user():
    form = registerForm()
    if request.method == 'POST':
        display_name = request.form.get('display_name')
        email = request.form.get('email')
        password = request.form.get('password')
        msg = Message(subject='Nieuwe registratie', sender='info@raadwiki.nl', recipients=['floris@florisdeboer.com'])
        msg.body = "Er is een nieuwe registratie. Graag goedkeuren."
        mail.send(msg)
        try:
            auth.create_user(email=email, password=password, display_name=display_name, disabled=True)
            msg = Message(subject='We gaan je registratie bekijken', sender='info@raadwiki.nl', recipients=[email])
            msg.body = "Alvast van harte welkom " + display_name + " en leuk dat je mee wil helpen! Een beheerder gaat je aanvraag zometeen goedkeuren. Je ontvangt dan nader bericht."
            mail.send(msg)
            return render_template('auth/approval.html')
        except:
            flash('Oei, probeer opnieuw met een andere email. Deze bestaat al.')
            return render_template('auth/register.html', form=form)
    else:
        return render_template('auth/register.html', form=form)

@bp.route('/login', methods=['POST', 'GET'])
def rw_login_user():
    form = loginForm()
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
            return redirect(url_for('zalen.index'))

    return render_template('auth/login.html', form=form)

@bp.route('/logout')
def logout():
    if('user' in session):
        session.pop('user')
        return redirect(url_for('auth.rw_login_user'))
    else:
        return redirect(url_for('auth.rw_login_user'))

#export GOOGLE_APPLICATION_CREDENTIALS=/app/raadzaalwiki-firebase-adminsdk-mun9y-a8eac2ba13.json
#https://raadzaalwiki.firebaseapp.com/__/auth/handler

