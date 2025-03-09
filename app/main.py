# add two more article fetching
# add update, deletion
# add login

from enum import Enum

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

import os

class ArticleName(str, Enum):
    morning = "morning"
    coffee = "coffee"
    work = "Now get to work"

app = FastAPI()

@app.get("/articles/morning", response_class=PlainTextResponse)
async def read_morning_file():
    file_path = r"G:\Projects\todo-api\app\morning.txt"
    try:
        with open(file_path, "r") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"Error reading file: {str(e)}"

@app.get("/articles/{article_name}")
async def get_articles(article_name: ArticleName):
    if article_name is ArticleName.morning:
        return {"article_anme": article_name, "message": "Your very thorough morning rutine"}
    
    if article_name.value == "coffee":
        return {"article_anme": article_name, "message": "Good ol' sip"}
    
    return {"article_anme": article_name, "message": "Now get to work"}