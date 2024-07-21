from flask_sqlalchemy import SQLAlchemy
from src.services.verify import Verificator

verificator = Verificator()
db = SQLAlchemy()
