from flask import Blueprint

bp = Blueprint('zalen', __name__)

from app.zalen import routes