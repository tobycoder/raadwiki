from flask import Flask, session, redirect, url_for
from flask_wtf import CSRFProtect
import os
from flask_mail import Mail
from os.path import join, dirname, realpath
import firebase_admin

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "adsfjkashdfkjsgdfksdjhhksdhgkjsdhkjgdsfhgfdlskjsdljg"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/images')
UPLOAD_FOLDER_STATIC = 'static/images'
app = Flask(__name__)
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_STATIC'] = UPLOAD_FOLDER_STATIC
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)
# Initialize Flask extensions here

app.app_context().push()
CSRFProtect(app)

# Register blueprints here

from app.zalen import bp as zalen_bp
app.register_blueprint(zalen_bp, url_prefix='/zalen')

from app.add import bp as add_bp
app.register_blueprint(add_bp, url_prefix='/add')

from app.viewer import bp as viewer_bp
app.register_blueprint(viewer_bp, url_prefix='/viewer')

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

from app.renovaties import bp as reno_bp
app.register_blueprint(reno_bp, url_prefix='/renovaties')

from app.dashboard import bp as dashboard_bp
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

from app.master import bp as master_bp
app.register_blueprint(master_bp, url_prefix='/master')

from app.motiemojo import bp as motiemojo_bp
app.register_blueprint(motiemojo_bp, url_prefix='/motiemojo')

@app.route('/')
def test_page():
    return redirect(url_for('zalen.index'))

