from app import app
from app.auth import bp
from firebase_admin import auth
from app.forms.login import registerForm, loginForm, approvalForm, passwordReset, replyForm
from flask import render_template, request, url_for, redirect, flash, session
from flask_mail import Message
import requests
import json
from app import mail
import os
from app.auth.decorators import master_required, login_required
from werkzeug.utils import secure_filename
import uuid as uuid
from app.authentication import raadzalen, renovaties, messages, replies
from google.cloud.firestore import FieldFilter
from app.functions import count_raadzalen_by_user, count_renovaties_by_user, count_entries

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
        avatar = request.files.get('avatar')
        # Grab image name
        avatar_name = secure_filename(avatar.filename)
        # Set UUID
        avatar_path = str(uuid.uuid1()) + "_" + avatar_name
        avatar.save(os.path.join(app.config['UPLOAD_FOLDER'], avatar_path))
        user = auth.create_user(email=email, password=password, display_name=display_name, disabled=True, photo_url=os.environ.get('SITE_BASE_URL') + "/" + app.config['UPLOAD_FOLDER_STATIC'] + "/" + avatar_path)
        msg = Message(subject='We gaan je registratie bekijken', sender=master_email, recipients=[email])
        msg.body = "Alvast van harte welkom " + display_name + " en leuk dat je mee wil helpen! Een beheerder gaat je aanvraag zometeen goedkeuren. Je ontvangt dan nader bericht."
        mail.send(msg)
        msg_2 = Message(subject='Nieuwe registratie', sender=master_email,
                      recipients=[send_master])
        msg_2.html = "<h1>Er is een nieuwe registratie. Graag goedkeuren.</h1><a href='http://127.0.0.1:5000/auth/{a}/approval'>Keur hier lokaal goed</a><a href='http://borisdefloer.pythonanywhere.com/auth/{a}/approval'>Keur hier online goed</a>".format(a=user.uid)
        mail.send(msg_2)
        return render_template('auth/approval.html', photo=user.photo_url)
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
            flash("Je hebt waarschijnlijk verkeerde gegevens ingevuld. Probeer opnieuw." + str(callback))
            return render_template('auth/login.html', form=form)
        else:
            flash('Welkom, ' + email)
            session['user'] = email
            return redirect(url_for('dashboard.index'))

    return render_template('auth/login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    if session['user']:
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

@bp.route('/<id>/password-reset', methods=['POST', 'GET'])
@login_required
def password_reset(id):
    user = auth.get_user(id)
    form = passwordReset()
    if session['user']:
        if session['user'] == user.email or session['user'] == os.environ.get('MASTER_EMAIL'):
            if request.method == 'POST':
                if request.form.get('password') == request.form.get('password_repeat'):
                    user = auth.update_user(id, password=request.form.get('password'))
                    flash('Succesvol je wachtwoord gewijzigd!')
                    return redirect(url_for('dashboard.index'))
            else:
                return render_template('auth/password_reset.html', id=id, form=form)
        else:
            flash('Je bent niet ingelogd met het account waar je het wachtwoord voor wil wijzigen')
            return redirect(url_for('dashboard.index'))
    else:
        flash('Je moet ingelogd zijn om je wachtwoord te wijzigen')
        return redirect(url_for('dashboard.index'))

@bp.route('/edit-profile', methods=['POST', 'GET'])
@login_required
def edit_profile():
    form = registerForm()
    user_id = auth.get_user_by_email(session['user'])
    if request.method == 'POST':
        display_name = request.form.get('display_name')
        email = request.form.get('email')
        password = request.form.get('password')
        avatar = request.files.get('avatar')
        # Grab image name
        avatar_name = secure_filename(avatar.filename)
        # Set UUID
        avatar_path = str(uuid.uuid1()) + "_" + avatar_name
        avatar.save(os.path.join(app.config['UPLOAD_FOLDER'], avatar_path))
        user = auth.update_user(user_id.uid,
                                email=email,
                                password=password,
                                display_name=display_name,
                                disabled=False,
                                photo_url=os.environ.get('SITE_BASE_URL') + "/" + app.config['UPLOAD_FOLDER_STATIC'] + "/" + avatar_path
                                )
        return redirect(url_for('auth.edit.profile'))
    else:
        return render_template('auth/edit_profile.html', form=form, user_id=user_id)

@bp.route('/mijn-bijdragen')
@login_required
def bijdragen():
    rz_query = raadzalen.where(filter=FieldFilter('auteur', '==', session['user'])).get()
    ren_query = renovaties.where(filter=FieldFilter('auteur', '==', session['user'])).get()
    count = count_raadzalen_by_user(session['user'])
    count_ren = count_renovaties_by_user(session['user'])
    return render_template('auth/bijdragen.html', count=count, count_ren=count_ren, rz_query=rz_query, ren_query=ren_query)

@bp.route('/berichten')
@login_required
def berichten():
    berichten = messages.where(filter=FieldFilter('to', '==', session['user'])).get()
    return render_template('inbox.html', berichten=berichten, get_user=auth.get_user_by_email)

@bp.route('/bericht/<id>')
@login_required
def single_berichten(id):
    bericht = messages.document(id).get()
    berichten = messages.where(filter=FieldFilter('to', '==', session['user'])).get()
    reply_content = replies.where(filter=FieldFilter('thread_id', '==', id)).get()
    form = replyForm()
    return render_template('auth/berichten.html', berichten=berichten, get_user=auth.get_user_by_email, bericht=bericht.to_dict(), form=form, id=bericht.id, replies=reply_content)

@bp.route('/reply/<id>', methods=['POST', 'GET'])
@login_required
def reply(id):
    bericht = messages.document(id).get()
    if request.method == 'POST':
        data = {
            'from': session['user'],
            'to': bericht.to_dict()['from'],
            'content': request.form.get('content'),
            'subject': bericht.to_dict()['subject'],
            'thread_id': id
        }
        replies.add(data)
        return redirect(url_for('auth.single_berichten', id=id))

@app.context_processor
def get_profile_pic():
    if('user' in session):
        user = auth.get_user_by_email(session['user'])
        avatar_url = user.photo_url
        if avatar_url:
            return {'avatar_url': avatar_url}
        else:
            return {'avatar_url': 'florisdeboer.com'}
    else:
        return {'avatar_url': 'florisdeboer.com'}

@app.context_processor
def get_user_id():
    if('user' in session):
        user = auth.get_user_by_email(session['user'])
        user_id = user.uid
        if user_id:
            return {'global_user_id': user_id}
        else:
            return {'global_user_id': 'none'}
    else:
        return {'global_user_id': 'none'}

@app.context_processor
def get_global_url():
    return {'SITE_BASE_URL' : os.environ.get('SITE_BASE_URL')}