from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from core.services import Verificator
verificator = Verificator()
