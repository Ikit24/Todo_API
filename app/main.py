from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import List, Annotated, Optional
from enum import Enum

from fastapi.security import OAuth2PasswordRequestForm


from .user_auth import (
    User, fake_users_db, fake_hash_password, 
    get_current_active_user, UserInDB
)

app = FastAPI()

# Get a list of tasks, filter them by status and get the details of each one.

class ArtucleStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class Article(BaseModel):
    id: int
    name: str
    price: float
    status: ArticleStatus = ArticleStatus.DRAFT

articles = []

# Authentication endpoints
@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)

    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user

# Article endpoints
@app.get("/articles", response_model=List[Article])
async def read_articles():
    return articles

@app.post("/articles", response_model=Article)
async def create_article(article: Article):
    articles.append(article)
    return article

@app.put("/articles/{article_id}", response_model=Article)
async def update_article(article_id: int, article: Article):
    for i, existing_article in enumerate(articles):
        if existing_article.id == article_id:
            articles[i] = article
            return article
    raise HTTPException(status_code=404, detail="Article not found")

@app.delete("/articles/{article_id}")
async def delete_article(article_id: int):
    for i, existing_article in enumerate(articles):
        if existing_article.id == article_id:
            del articles[i]
            return {"message": "Article deleted"}
    raise HTTPException(status_code=404, detail="Article not found")