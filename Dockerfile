# Dockerfile multi-stage para produção (usado por Google, Amazon, etc.)
FROM python:3.11-slim AS base

# Configurações básicas
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Estágio de build
FROM base AS builder

WORKDIR /build
COPY requirements.txt pyproject.toml ./
RUN pip install --user -r requirements.txt

# Estágio de produção
FROM base AS production

# Cria usuário não-root para segurança
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copia dependências do estágio anterior
COPY --from=builder /root/.local /home/appuser/.local

# Configura PATH para usuário
ENV PATH=/home/appuser/.local/bin:$PATH

WORKDIR /app

# Copia código da aplicação
COPY src/ ./src/
COPY app.py .
COPY .env.example .env

# Muda proprietário dos arquivos
RUN chown -R appuser:appuser /app

# Muda para usuário não-root
USER appuser

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Expõe porta
EXPOSE 5000

# Comando padrão
CMD ["python", "app.py"]