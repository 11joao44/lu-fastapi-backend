# syntax=docker/dockerfile:1

########################################
# Etapa 1: Build das dependências
########################################
FROM python:3.12-slim AS builder

WORKDIR /app

# Dependências de sistema para compilar extensões (p. ex. asyncpg)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

# Poetry
RUN pip install --upgrade pip \
    && pip install poetry

# Cache de dependências
COPY pyproject.toml poetry.lock* /app/

# Instala apenas dependências de runtime
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Código da aplicação
COPY . /app

########################################
# Etapa 2: Imagem final de execução
########################################
FROM python:3.12-slim AS runtime

WORKDIR /app

# Cria usuário não-root
RUN useradd --create-home appuser

# Copia libs e binários
COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=builder /usr/local/bin /usr/local/bin
# Copia aplicação
COPY --from=builder /app /app

# Ajusta permissões
RUN chown -R appuser:appuser /app

USER appuser

ENV PYTHONUNBUFFERED=1 \
    UVICORN_WORKERS=4 \
    UVICORN_RELOAD=0

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", \
     "--host", "0.0.0.0", "--port", "8000", \
     "--workers", "${UVICORN_WORKERS}", \
     "--reload", "${UVICORN_RELOAD}"]
