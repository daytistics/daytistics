from fastapi import FastAPI
from enum import Enum

app = FastAPI()

arr = [f"Item {i}" for i in range(0, 20)]

class ProgrammingLanguage(str, Enum):
    python = ".py"
    javascript = ".js"
    rust = ".rs"

@app.get("/")
async def root():
    return {"message": "Hello Dad"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item": arr[item_id]}

@app.get("/lang/{lang}")
async def get_language(lang: ProgrammingLanguage):
    return {"lang": lang}