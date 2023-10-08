from flask import Blueprint

bp = Blueprint('renovaties', __name__)

from app.renovaties import routes