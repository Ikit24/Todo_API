# add login
# create both users and tasks.
# be able to update tasks (their status) and even delete them.
# Get a list of tasks, filter them by status and get the details of each one.
# fastapi dev main.py - to start the server

from typing import Annotated

from pydantic import BaseModel
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

from .user_auth import *

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Article(BaseModel):
    id: int
    name: str
    price: float

def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user


@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

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