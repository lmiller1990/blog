import os
from pathlib import Path
import shutil
import markdown
from datetime import datetime
from typing import TypedDict


# articles
def get_all_articles(path: str) -> list[str]:
    entries = os.listdir(path)
    return [entry for entry in entries if os.path.isdir(os.path.join(path, entry))]


class Article(TypedDict):
    title: str
    published: datetime
    description: str
    markdown: str
    slug: str


def extract_meta(text: str) -> tuple[dict[str, str], str]:
    meta: dict[str, str] = dict()

    # if lines[0].strip() != "+++":
    #     raise RuntimeError("Expected first line to be +++")
    # lines = lines[1:]
    # while lines[0].strip() != "+++":
    #     key, value = lines[0].strip().split(":", 1)
    #     meta[key.strip()] = value.strip()
    #     lines = lines[1:]

    # lines = lines[1:]
    # return meta, lines
    # Split the text using the '+++' delimiters
    parts = text.split("+++")

    if len(parts) < 3:
        raise ValueError(
            "The input text does not contain valid metadata delimiters '+++'"
        )

    # The metadata is in the first segment after splitting
    metadata = parts[1].strip().split("\n")
    for line in metadata:
        key, value = line.strip().split(":", 1)
        meta[key.strip()] = value.strip()

    # The content (HTML) is in the parts after the metadata
    content = "".join(parts[2:]).strip()

    return meta, content


def read_content(path: str, slug: str) -> Article:
    with open(path, "r") as file:
        lines = file.read()
        meta, lines = extract_meta(lines)
        return {
            "title": meta["title"],
            "description": meta["description"],
            "markdown": lines,
            "published": datetime.strptime(meta["published"], "%Y-%m-%d"),
            "slug": slug,
        }


def build_articles(article_path: str, articles: list[str]) -> list[Article]:
    return [
        read_content(os.path.join(article_path, article, "index.md"), slug=article)
        for article in articles
    ]


def main():
    artpath = os.path.join(os.getcwd(), "articles")
    slugs = get_all_articles(artpath)
    articles = build_articles(artpath, slugs)

    if Path(os.path.join(os.getcwd(), "static")).exists():
        shutil.rmtree("static/articles")

    os.makedirs(os.path.join("static", "articles"), exist_ok=True)
    for article in articles:
        html = markdown.markdown(article["markdown"], extensions=["fenced_code"])
        with open(
            os.path.join("static", "articles", f"{article['slug']}.html"), "w"
        ) as f:
            f.write(html)


if __name__ == "__main__":
    main()
