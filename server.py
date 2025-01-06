import os

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from build import all_content


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def read_html(slug: str, content_dir: str) -> str:
    with open(os.path.join(os.getcwd(), "static", content_dir, f"{slug}.html")) as f:
        return f.read()


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/articles")
def articles(request: Request):
    all = all_content("articles")
    return templates.TemplateResponse(
        request=request,
        name="articles_index.html",
        context={"articles": all, "content_dir": "articles"},
    )


@app.get("/musings")
def musings(request: Request):
    all = all_content("musings")
    return templates.TemplateResponse(
        request=request,
        name="articles_index.html",
        context={"articles": all, "content_dir": "musings"},
    )


@app.get("/books")
def books(request: Request):
    return templates.TemplateResponse(request=request, name="books.html")

@app.get("/contact")
def contact(request: Request):
    return templates.TemplateResponse(request=request, name="contact.html")


@app.get("/articles/{slug}", response_class=HTMLResponse)
def read_article(request: Request, slug: str):
    try:
        content = read_html(slug, "articles")
        return templates.TemplateResponse(
            request=request, name="article.html", context={"content": content}
        )
    except Exception as err:
        print(err)


@app.get("/musings/{slug}", response_class=HTMLResponse)
def read_musings(request: Request, slug: str):
    try:
        content = read_html(slug, "musings")
        return templates.TemplateResponse(
            request=request, name="article.html", context={"content": content}
        )
    except Exception as err:
        print(err)
