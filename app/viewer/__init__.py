from flask import Blueprint

bp = Blueprint('viewer', __name__)

from app.viewer import routes