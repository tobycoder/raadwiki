from flask import Blueprint

bp = Blueprint('motiemojo', __name__)

from app.motiemojo import routes