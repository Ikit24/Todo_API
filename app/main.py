# add login
# create both users and tasks.
# be able to update tasks (their status) and even delete them.
# Get a list of tasks, filter them by status and get the details of each one.
# fastapi dev main.py - to start the server

from pydantic import BaseModel
from fastapi import FastAPI

class Article(BaseModel):
    id: int
    name: str
    price: float

app = FastAPI()

articles = {}

@app.get("/")
def welcome():
    return {"message": "Welcome to my first FastAPI application!"}

@app.get("/articles", response_model=list[Article])
async def read_articles():
    return list(articles.values())

@app.post("/articles", response_model=Article)
async def create_article(article: Article):
    articles[article.id] = article
    return article

@app.put("/articles/{article_id}", response_model=Article)
async def update_article(article_id: int, article: Article):
    articles[article_id] = article
    return article

@app.delete("/articles/{article_id}")
async def delete_article(article_id: int):
    del articles[article_id]
    return {"message": "Article deleted"}