from typing import Union
import os

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def read_html(slug: str) -> str:
    with open(os.path.join(os.getcwd(), "static", "articles", f"{slug}.html")) as f:
        return f.read()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/articles/{slug}", response_class=HTMLResponse)
def read_article(request: Request, slug: str):
    content = read_html(slug)
    return templates.TemplateResponse(
        request=request, name="article.html", context={"content": content}
    )
