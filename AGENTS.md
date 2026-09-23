# Authoring a New Blog Post

This guide explains the workflow for adding a new article (or musings) to the site.

## 1. Create a directory

All posts live under either `articles/` or `musings/`. Each post is represented by its own sub‑directory named after the slug you want in the URL.

```bash
# Example: a new article called *my-first-post*
mkdir -p articles/my-first-post
```

The directory can contain any supporting assets (images, data files, etc.). They will be copied to the corresponding `static/` folder when the site is built.

## 2. Add an `index.md`

Inside the new directory create a file called `index.md`. The first part of the file must be front‑matter surrounded by `+++` lines. The required keys are:

| Key | Type | Example |
|-----|------|---------|
| title | string | `My First Post` |
| published | date (`YYYY-MM-DD`) | `2026-09-23` |
| description | string | A short blurb used in the RSS feed and meta tags |

After the closing `+++`, write the article body using Markdown.

```markdown
+++
title: My First Post
published: 2026-09-23
description: An introductory post about the new blog workflow
image: https://example.com/preview.png
+++

## Hello World

This is my first post!
```

The `image` field is optional but useful for social previews.

## 3. Compile Markdown to HTML

The repository ships a small Python helper (`build.py`) that converts all Markdown files into static HTML pages under the `static/` directory.

```bash
# From the project root
python build.py
```

This will:
1. Read every sub‑directory of `articles/` and `musings/`.
2. Parse the front‑matter, sort posts by date, and convert the Markdown body to HTML using the `markdown` package with fenced code blocks, tables, and KaTeX support.
3. Write each article as `<slug>.html` inside `static/articles/` or `static/musings/`.

You can verify that the new post appears by opening `static/articles/my-first-post.html` in a browser.

---

### Tips
- Keep the slug short and URL‑friendly (lowercase, hyphens). It becomes part of the path.
- If you add images or other assets inside the post directory, they will be copied automatically when running `python build.py`.
- The `build.py` script is idempotent; run it after every change to regenerate all pages.

Happy writing!