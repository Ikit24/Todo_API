# add update, deletion
# add login
# fastapi dev main.py - to start the server

from enum import Enum

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

import os

class ArticleName(str, Enum):
    morning = "morning"
    coffee = "coffee"
    motivation = "motivation"

app = FastAPI()

@app.get("/articles/{article_type}", response_class=PlainTextResponse)
async def read_article_file(article_type: str):
    file_mapping = {
        "morning": r"G:\Projects\todo-api\app\morning.txt",
        "coffee": r"G:\Projects\todo-api\app\coffee.txt",
        "motivation": r"G:\Projects\todo-api\app\motivation.txt"
    }

    file_path = file_mapping.get(article_type)
    if file_path is None:
        return f"Invalid article type: {article_type}"
    
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