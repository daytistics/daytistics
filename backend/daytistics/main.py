from fastapi import FastAPI

from daytistics.graphql import setup_graphql
from daytistics.database import setup_db

app = FastAPI()

setup_db()
setup_graphql(app)
