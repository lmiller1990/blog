FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    chromium \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

RUN npm run tailwind:build

RUN uv run python build.py

ARG SKIP_PDF=false
RUN if [ "$SKIP_PDF" != "true" ]; then \
      node scripts/generate-resume-pdf.mjs; \
    else \
      echo "Skipping PDF generation (SKIP_PDF=true)"; \
    fi

FROM python:3.12-slim AS runtime

WORKDIR /app

COPY --from=builder /app/.venv ./.venv
COPY --from=builder /app/static ./static
COPY --from=builder /app/templates ./templates
COPY --from=builder /app/server.py ./
COPY --from=builder /app/build.py ./
COPY --from=builder /app/pyproject.toml ./
COPY --from=builder /app/uv.lock ./

EXPOSE 7777

CMD [".venv/bin/fastapi", "run", "server.py", "--port", "7777", "--host", "0.0.0.0"]
