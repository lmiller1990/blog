import os

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from build import all_articles


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def read_html(slug: str) -> str:
    with open(os.path.join(os.getcwd(), "static", "articles", f"{slug}.html")) as f:
        return f.read()


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/articles")
def articles(request: Request):
    all = all_articles()
    return templates.TemplateResponse(
        request=request, name="articles_index.html", context={"articles": all}
    )


@app.get("/articles/{slug}", response_class=HTMLResponse)
def read_article(request: Request, slug: str):
    content = read_html(slug)
    return templates.TemplateResponse(
        request=request, name="article.html", context={"content": content}
    )
