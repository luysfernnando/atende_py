# Makefile para automação de tarefas (usado por Netflix, Uber, etc.)

.PHONY: help install install-dev test lint format type-check clean run docker-build docker-run

# Variáveis
PYTHON = python3
PIP = pip
VENV = chatbotenv
SRC_DIR = src
TEST_DIR = tests

help: ## Mostra esta ajuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instala dependências básicas
	$(PIP) install -e .

install-dev: ## Instala dependências de desenvolvimento
	$(PIP) install -e ".[dev,ai]"
	pre-commit install

test: ## Executa todos os testes
	pytest $(TEST_DIR)/ -v

test-unit: ## Executa apenas testes unitários
	pytest $(TEST_DIR)/ -v -m "unit"

test-integration: ## Executa testes de integração
	pytest $(TEST_DIR)/ -v -m "integration"

test-coverage: ## Executa testes com coverage
	pytest $(TEST_DIR)/ --cov=$(SRC_DIR) --cov-report=html --cov-report=term

lint: ## Executa linting (flake8)
	flake8 $(SRC_DIR) $(TEST_DIR)

format: ## Formata código com black e isort
	black $(SRC_DIR) $(TEST_DIR)
	isort $(SRC_DIR) $(TEST_DIR)

format-check: ## Verifica formatação sem alterar
	black --check $(SRC_DIR) $(TEST_DIR)
	isort --check-only $(SRC_DIR) $(TEST_DIR)

type-check: ## Verifica tipos com mypy
	mypy $(SRC_DIR)

quality: format lint type-check test ## Executa todas as verificações de qualidade

clean: ## Limpa arquivos temporários
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/

run: ## Executa a aplicação
	$(PYTHON) app.py

run-prod: ## Executa com gunicorn (produção)
	gunicorn --bind 0.0.0.0:5000 --workers 4 app:app

docker-build: ## Constrói imagem Docker
	docker build -t atende-py .

docker-run: ## Executa container Docker
	docker run -p 5000:5000 --env-file .env atende-py

setup-dev: install-dev ## Configura ambiente de desenvolvimento completo
	@echo "🚀 Ambiente de desenvolvimento configurado!"
	@echo "📝 Execute 'make help' para ver comandos disponíveis"

ci: format-check lint type-check test ## Pipeline de CI/CD
	@echo "✅ Todas as verificações passaram!"