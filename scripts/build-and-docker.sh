#!/usr/bin/env bash
set -euo pipefail

echo "=== Generating resume PDF locally ==="
npm run resume:pdf

echo "=== Building Docker image (SKIP_PDF=true) ==="
docker build --build-arg SKIP_PDF=true "$@" .

docker buildx build \
  --build-arg SKIP_PDF=true \
  --platform linux/amd64 \
  --load \
  -t lachlanmillerdev/blog .


docker push lachlanmillerdev/blog 