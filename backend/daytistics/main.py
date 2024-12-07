from fastapi import FastAPI
import dotenv

from daytistics.graphql import setup_graphql
from daytistics.database import setup_db

app = FastAPI()

dotenv.load_dotenv()
setup_db()
setup_graphql(app)
