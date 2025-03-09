from enum import Enum

from fastapi import FastAPI

class ArticleName(str, Enum):
    morning = "morning"
    coffee = "coffee"
    work = "Now get to work"

app = FastAPI()

@app.get("/articles/{article_name}")
async def get_articles(article_name: ArticleName):
    if article_name is ArticleName.morning:
        return {"article_anme": article_name, "message": "Your very thorough morning rutine"}
    
    if article_name.value == "coffee":
        return {"article_anme": article_name, "message": "Good ol' sip"}
    
    return {"article_anme": article_name, "message": "Now get to work"}