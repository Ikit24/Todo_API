# be able to update tasks (their status) and even delete them.
# Get a list of tasks, filter them by status and get the details of each one.
# fastapi dev main.py - to start the server

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Article(BaseModel):
    id: int
    name: str
    price: float

with open("user_auth.py") as file:
    exec(file.read())

articles = []

@app.get("/articles", response_model=List[Article])
async def read_articles():
    return articles

@app.post("/articles", response_model=Article)
async def create_article(article: Article):
    articles.append(article)
    return article

@app.put("/articles/{article_id}", response_model=Article)
async def update_article(article_id: int, article: Article):
    if article_id < 0 or article_id >= len(articles):
        raise HTTPException(status_code=404, detail="Article not found")

    articles[article_id] = article
    return article

@app.delete("/articles/{article_id}")
async def delete_article(article_id: int):
    if article_id < 0 or article_id >= len(articles):
        raise HTTPException(status_code=404, detail="Article not found")

    del articles[article_id]
    return {"message": "Article deleted"}