# 🤖 Atende.py

> **Sistema inteligente de chatbot para WhatsApp com agendamento automatizado**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com)
[![Twilio](https://img.shields.io/badge/Twilio-WhatsApp-red.svg)](https://twilio.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.md)

---

## ✨ **Funcionalidades**

🎯 **Conversação Inteligente**  
• Detecção automática de intenções (saudações, agendamentos, cancelamentos)  
• Respostas contextuais personalizadas  
• Histórico de conversas persistente  

📅 **Agendamento Automatizado**  
• Coleta de dados do paciente via chat  
• Validação de horários disponíveis  
• Confirmação automática de consultas  

🔄 **Gestão Completa**  
• Reagendamento via WhatsApp  
• Cancelamento com confirmação  
• Notificações e lembretes  

---

## 🛠️ **Tecnologias**

| Frontend | Backend | Database | Cloud |
|----------|---------|----------|-------|
| WhatsApp | Flask | SQLite | Twilio |
| HTML/CSS | Python 3.13 | SQLAlchemy | Docker |

**Arquitetura Clean**: MVC + Repository Pattern + Dependency Injection

---

## 🚀 **Início Rápido**

### **Pré-requisitos**
```bash
Python 3.9+ • Conta Twilio • Git
```

### **Instalação**
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/atende-py.git
cd atende-py

# Configure o ambiente
make setup-dev

# Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas credenciais Twilio
```

### **Execução**
```bash
# Desenvolvimento
make run

# Produção
make run-prod

# Docker
make docker-build && make docker-run
```

---

## ⚙️ **Configuração**

### **Variáveis de Ambiente**
```env
TWILIO_ACCOUNT_SID=seu_account_sid
TWILIO_AUTH_TOKEN=seu_auth_token  
TWILIO_PHONE_NUMBER=+14155238886
```

### **Webhook WhatsApp**
```
https://seu-dominio.com/webhook/whatsapp
```

---

## 📋 **Comandos**

```bash
make help          # Lista todos os comandos
make test           # Executa testes
make format         # Formata código
make quality        # Verifica qualidade
make clean          # Limpa arquivos temporários
```

---

## 🏗️ **Arquitetura**

```
src/
├── controllers/    # Camada de apresentação
├── services/       # Regras de negócio  
├── models/         # Entidades de domínio
├── database/       # Persistência de dados
└── utils/          # Utilitários gerais
```

**Padrões aplicados**: SOLID, Clean Architecture, Repository Pattern

---

## 🧪 **Testes**

```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=src --cov-report=html

# Apenas unitários
pytest -m unit

# Apenas integração
pytest -m integration
```

---

## 📝 **API**

### **Enviar Mensagem**
```http
POST /mensagem
Content-Type: application/json

{
  "user_id": "5511999999999",
  "mensagem": "Quero agendar uma consulta"
}
```

### **Webhook WhatsApp**
```http
POST /webhook/whatsapp
Content-Type: application/x-www-form-urlencoded

Body=mensagem&From=whatsapp:+5511999999999
```

---

## 🔄 **Fluxos de Conversação**

**Agendamento**
```
👤 "Quero agendar"
🤖 "Qual seu nome?"
👤 "João Silva"  
🤖 "Qual data deseja?"
👤 "15/06/2025"
🤖 "Consulta agendada! ✅"
```

**Reagendamento**
```
👤 "Reagendar consulta"
🤖 "Nova data?"
👤 "20/06/2025"
🤖 "Reagendado! ✅"
```

---

## 🐳 **Docker**

```dockerfile
# Build
docker build -t atende-py .

# Run
docker run -p 5000:5000 --env-file .env atende-py
```

---

## 🤝 **Contribuindo**

1. **Fork** o projeto
2. **Crie** uma branch (`git checkout -b feature/nova-funcionalidade`)
3. **Commit** suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. **Push** para a branch (`git push origin feature/nova-funcionalidade`)
5. **Abra** um Pull Request

---

## 📄 **Licença**

Este projeto está licenciado sob a **MIT License** - veja [LICENSE.md](LICENSE.md) para detalhes.

---

## 👨‍💻 **Autor**

**Luys Fernnando**  
🐙 [GitHub](https://github.com/luysfernnando)
💼 [LinkedIn](https://linkedin.com/in/luysfernnando)

---

<div align="center">

**⭐ Se este projeto te ajudou, deixe uma estrela!**

*Desenvolvido com ❤️ usando Python e Clean Architecture*

</div>
