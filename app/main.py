import os 
os.environ["HF_HOME"] = "D:/models"
from transformers import pipeline

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.models import pydantic
from app.zero_shot.intent import find_intent
from app.config.intent_connector import query_connector
from app.llm.chain import llm_responce



app = FastAPI()
app.mount("/app/static", StaticFiles(directory="app/static"), name="static")

template = Jinja2Templates(directory="app/templates")


@app.get("/")
async def main(request: Request):
    return template.TemplateResponse("index.html" ,{"request" : request})

@app.post("/display-data")
async def display_data(user: pydantic.User):
    return {"redirect_url" : f"/display/{user.name}/{user.email}/{user.age}"}

@app.get("/display/{name}/{email}/{age}", response_class=HTMLResponse)
async def display_page(request: Request, name: str, email: str, age: int):
    user = {"name": name, "email": email, "age": age}
    return template.TemplateResponse("display.html", {"request": request, "user": user})

@app.post("/query")
async def query(q: pydantic.UserQuery):
    intent = find_intent(q.query)
    print(intent)
    db_result = query_connector(intent=intent, employee_id=24, query = q.query)
    print(db_result)
    # print(type(db_result))
    responce = llm_responce(q.query,db_result)
    print(responce)
    return {"answer": responce}