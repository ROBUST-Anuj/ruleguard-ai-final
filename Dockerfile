FROM node:20-slim AS frontend-build
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ backend/
COPY data/ data/
COPY scripts/ scripts/
COPY .env.example .env.example

COPY --from=frontend-build /app/frontend/dist frontend/dist

EXPOSE 8000

CMD ["sh", "-c", "python scripts/ingest.py && uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
