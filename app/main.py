# add update, deletion
# add login
# fastapi dev main.py - to start the server

from pydantic import BaseModel
from fastapi import FastAPI
from enum import Enum
from fastapi.responses import PlainTextResponse

class ArticleName(str, Enum):
    morning = "morning"
    coffee = "coffee"
    motivation = "motivation"

class Article(BaseModel):
    id: int
    name: str
    price: float

app = FastAPI()

articles = []

@app.get("/")
def welcome():
    return {"message": "Welcome to my first FastAPI application!"}

@app.get("/articles/{article_type}", response_class=PlainTextResponse)
async def get_articles(article_name: ArticleName):
    file_mapping = {
        "morning": r"G:\Projects\todo-api\app\morning.txt",
        "coffee": r"G:\Projects\todo-api\app\coffee.txt",
        "motivation": r"G:\Projects\todo-api\app\motivation.txt"
    }

    file_path = file_mapping.get(article_name)
    if file_path is None:
        return f"Invalid article type: {article_name}"
    
    try:
        with open(file_path, "r") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"Error reading file: {str(e)}"

@app.get("/articles", response_model=list[Article])
async def read_articles():
    return articles

@app.post("articles", response_model=Article)
async def create_article(article: Article):
    articles.append(article)
    return article

@app.put("/articles/{article_id}", response_model=Article)
async def update_article(article_id: int, article: Article):
    articles[article_id] = article
    return article

@app.delete("articles/{article_id}")
async def delete_article(article_id: int):
    del articles[article_id]
    return {"message": "Article deleted"}