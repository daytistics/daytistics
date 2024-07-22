from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from src.services.verify import Verificator
verificator = Verificator()

