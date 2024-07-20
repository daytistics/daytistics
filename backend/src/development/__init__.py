from flask import Blueprint

bp = Blueprint("dev", __name__)

from src.development import routes
