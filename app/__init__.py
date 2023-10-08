from flask import Flask, session, redirect, url_for
from flask_wtf import CSRFProtect
import os
from flask_mail import Mail

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "adsfjkashdfkjsgdfksdjhhksdhgkjsdhkjgdsfhgfdlskjsdljg"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
app.config.from_object(Config)
app.config['MAIL_SERVER']='smtp.transip.email'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
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

@app.route('/')
def test_page():
    return redirect(url_for('zalen.index'))

@app.context_processor
def utility_processor():
    def login_check():
        if('user' in session):
            return {'logged_in': True}
        else:
            return {'logged_in': False}
    return login_check()