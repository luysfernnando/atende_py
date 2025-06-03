# tests/README.md
# 🧪 Testes do Chatbot

Esta pasta contém todos os testes organizados do projeto, seguindo as melhores práticas de teste.

## 📁 Estrutura

```
tests/
├── __init__.py                     # Módulo Python
├── test_models.py                  # Testes unitários dos modelos
├── test_chatbot_integration.py     # Testes de integração E2E
├── run_all_tests.py               # Executador de todos os testes
└── README.md                      # Esta documentação
```

## 🚀 Como executar

### Todos os testes (recomendado)
```bash
python tests/run_all_tests.py
```

### Apenas testes unitários
```bash
python tests/test_models.py
```

### Apenas testes de integração
```bash
# IMPORTANTE: Inicie o servidor primeiro!
python app.py

# Em outro terminal:
python tests/test_chatbot_integration.py
```

## 📋 Tipos de teste

### 🧪 Testes Unitários (`test_models.py`)
- Testam modelos isoladamente
- Não precisam de servidor rodando
- Verificam lógica de negócio dos modelos

### 🔗 Testes de Integração (`test_chatbot_integration.py`)
- Testam o sistema completo end-to-end
- Precisam do servidor rodando (`python app.py`)
- Verificam APIs, banco de dados e fluxos completos

## ✅ O que é testado

- ✅ Criação e manipulação de modelos
- ✅ Estados da conversa
- ✅ Fluxo completo de marcação de consulta
- ✅ Persistência no banco SQLite
- ✅ APIs REST funcionando
- ✅ Histórico e estatísticas

## 🎯 Cobertura de testes

Os testes cobrem:
- **Modelos**: Consulta e Conversa
- **APIs**: Todas as 8 rotas principais
- **Banco**: Persistência e recuperação
- **Fluxos**: Conversa completa do usuário