from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from core.services.verification import Verificator
verificator = Verificator()

