from flask import Flask
from flask_wtf import CSRFProtect
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "adsfjkashdfkjsgdfksdjhhksdhgkjsdhkjgdsfhgfdlskjsdljg"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
app.config.from_object(Config)

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

@app.route('/test/')
def test_page():
    return '<h1>Testing the Flask Application Factory Pattern</h1>'
