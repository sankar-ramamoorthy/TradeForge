FROM node:22-bookworm-slim AS frontend-build

WORKDIR /frontend

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PYTHONUNBUFFERED=1
ENV TRADEFORGE_SERVE_FRONTEND=1

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY . .
COPY --from=frontend-build /frontend/dist ./frontend/dist

EXPOSE 8000

CMD ["sh", "-c", ".venv/bin/alembic upgrade head && exec .venv/bin/uvicorn src.app.api.application:app --host 0.0.0.0 --port 8000"]
