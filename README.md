# 🤖 Atende.py

> **Sistema inteligente de chatbot para WhatsApp com agendamento automatizado + Dashboard Web**

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

🌐 **Dashboard Web Modular**  
• Interface administrativa completa  
• Monitoramento de conversas em tempo real  
• Gestão de configurações Twilio  
• Estatísticas e relatórios detalhados  
• Histórico de conversas com busca  
• Gestão de consultas agendadas  

🔄 **Gestão Completa**  
• Reagendamento via WhatsApp  
• Cancelamento com confirmação  
• Notificações e lembretes  

---

## 🛠️ **Tecnologias**

| Frontend | Backend | Database | Cloud |
|----------|---------|----------|-------|
| Bootstrap 5 | Flask | SQLite | Twilio |
| JavaScript ES6 | Python 3.13 | SQLAlchemy | Docker |
| WhatsApp | RESTful API | Repository Pattern | Webhooks |

**Arquitetura Clean**: MVC + Repository Pattern + SOLID + Modular Design

---

## 🚀 **Início Rápido**

### **Pré-requisitos**
```bash
Python 3.9+ • Conta Twilio • Git
```

### **Instalação**
```bash
# Clone o repositório
git clone https://github.com/luysfernnando/atende-py.git
cd atende-py

# Configure o ambiente virtual
python -m venv chatbotenv
source chatbotenv/bin/activate  # Linux/Mac
# chatbotenv\Scripts\activate  # Windows

# Instale dependências
pip install -r requirements.txt

# Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas credenciais Twilio
```

### **Execução**
```bash
# Desenvolvimento
python app.py

# O servidor iniciará em:
# 🌐 Dashboard Web: http://localhost:5000
# 📱 API WhatsApp: http://localhost:5000/webhook/whatsapp
```

---

## 🌐 **Dashboard Web**

O sistema agora inclui uma **interface web completa** acessível em `http://localhost:5000`

### **Funcionalidades do Dashboard:**

🏠 **Visão Geral**
- Estatísticas em tempo real
- Monitoramento de sistema
- Status de conexão

⚙️ **Configurações**
- Gestão de credenciais Twilio
- Configuração automática do .env
- Validação de configurações

💬 **Conversas ao Vivo**
- Monitoramento em tempo real (futuro: WebSocket)
- Busca por histórico de usuário
- Detalhes completos de conversas
- Reinicialização de conversas

📊 **Estatísticas**
- Total de consultas agendadas
- Usuários únicos atendidos
- Consultas do dia atual
- Atualização automática (30s)

📅 **Consultas Agendadas**
- Listagem completa de consultas
- Filtros por período (hoje, semana, mês)
- Informações detalhadas dos pacientes
- Status de confirmação

---

## 📋 **API Endpoints**

### **🔥 Endpoints Principais**

#### **Dashboard Web**
```http
GET /                    # Dashboard principal
GET /static/<path>       # Arquivos estáticos (CSS, JS, imagens)
```

#### **Chatbot Core**
```http
POST /mensagem           # Processar mensagem do chatbot
GET /health             # Verificação de saúde do sistema
GET /config             # Obter configurações atuais (.env)
```

#### **Consultas**
```http
GET /consultas          # Listar todas as consultas
GET /consultas/<user_id> # Consultas de um usuário específico
```

#### **Conversas**
```http
GET /historico/<user_id>           # Histórico de conversa do usuário
GET /conversa/status/<user_id>     # Status atual da conversa
POST /conversa/reiniciar/<user_id> # Reiniciar conversa do usuário
```

#### **Estatísticas**
```http
GET /estatisticas       # Estatísticas completas do sistema
```

#### **WhatsApp (Twilio)**
```http
POST /webhook/whatsapp  # Webhook para receber mensagens do Twilio
POST /whatsapp/enviar   # Enviar mensagem direta via WhatsApp
```

### **📝 Exemplos de Uso**

#### **Enviar Mensagem para o Chatbot**
```http
POST /mensagem
Content-Type: application/json

{
  "user_id": "5511999999999",
  "mensagem": "Quero agendar uma consulta"
}
```

**Resposta:**
```json
{
  "resposta": "Olá! Vou ajudá-lo a agendar sua consulta. Qual o seu nome completo?",
  "estado": "aguardando_nome"
}
```

#### **Buscar Histórico de Conversa**
```http
GET /historico/5511999999999
```

**Resposta:**
```json
[
  {
    "remetente": "user",
    "mensagem": "Quero agendar uma consulta",
    "timestamp": "2025-06-03T18:30:00"
  },
  {
    "remetente": "bot", 
    "mensagem": "Qual o seu nome completo?",
    "timestamp": "2025-06-03T18:30:01"
  }
]
```

#### **Obter Estatísticas**
```http
GET /estatisticas
```

**Resposta:**
```json
{
  "total_consultas": 25,
  "usuarios_unicos": 18,
  "consultas_hoje": 3,
  "consultas_criadas_hoje": 5,
  "consultas_por_periodo": {
    "manhã": 8,
    "tarde": 12,
    "noite": 5
  }
}
```

#### **Webhook WhatsApp (Twilio)**
```http
POST /webhook/whatsapp
Content-Type: application/x-www-form-urlencoded

Body=Olá&From=whatsapp:+5511999999999&To=whatsapp:+14155238886
```

---

## ⚙️ **Configuração**

### **Variáveis de Ambiente (.env)**
```env
# Configurações do Twilio para WhatsApp
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=+14155238886

# Configurações da aplicação
FLASK_ENV=development
SECRET_KEY=sua-chave-secreta-aqui

# URL base para webhooks
BASE_URL=https://seu-dominio.com
```

### **Webhook WhatsApp**
Configure no painel do Twilio:
```
https://seu-dominio.com/webhook/whatsapp
```

---

## 🏗️ **Arquitetura Modular**

```
src/
├── controllers/        # Camada de apresentação (MVC)
│   ├── chatbot_controller.py
│   └── whatsapp_controller.py
├── services/          # Regras de negócio (Business Logic)
│   ├── chatbot_service.py
│   ├── ai_service.py
│   └── whatsapp_service.py
├── models/            # Entidades de domínio (Domain Models)
│   ├── consulta.py
│   └── conversa.py
├── database/          # Persistência de dados (Repository Pattern)
│   ├── database_manager.py
│   ├── consulta_repository.py
│   └── conversa_repository.py
└── utils/             # Utilitários gerais

static/                # Assets da interface web
├── css/
│   └── dashboard.css  # Estilos modulares com variáveis CSS
├── js/
│   └── dashboard.js   # JavaScript modular seguindo SOLID
└── images/

templates/             # Templates HTML
└── dashboard.html     # Interface principal responsive
```

**Padrões Aplicados:**
- ✅ **SOLID** - Responsabilidade única, aberto/fechado, etc.
- ✅ **Repository Pattern** - Abstração de dados
- ✅ **Dependency Injection** - Inversão de dependências
- ✅ **MVC** - Separação de responsabilidades
- ✅ **Clean Architecture** - Camadas bem definidas

---

## 🔄 **Fluxos de Conversação**

**Agendamento Completo**
```
👤 "Quero agendar"
🤖 "Qual seu nome?"
👤 "João Silva"  
🤖 "Qual data deseja? (DD/MM/AAAA)"
👤 "15/06/2025"
🤖 "Qual período? (manhã/tarde/noite)"
👤 "manhã"
🤖 "✅ Consulta agendada para João Silva em 15/06/2025 (manhã)"
```

**Reagendamento**
```
👤 "Reagendar consulta"
🤖 "Nova data?"
👤 "20/06/2025"
🤖 "✅ Consulta reagendada para 20/06/2025"
```

**Cancelamento**
```
👤 "Cancelar consulta"
🤖 "Confirma o cancelamento? (sim/não)"
👤 "sim"
🤖 "✅ Consulta cancelada com sucesso"
```

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

# Teste específico
pytest tests/test_chatbot_integration.py
```

---

## 🐳 **Docker**

```dockerfile
# Build da imagem
docker build -t atende-py .

# Executar container
docker run -p 5000:5000 --env-file .env atende-py

# Docker Compose (recomendado)
docker-compose up -d
```

---

## 🚀 **Deploy**

### **Produção com Gunicorn**
```bash
# Instalar Gunicorn
pip install gunicorn

# Executar
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### **Nginx + SSL**
```nginx
server {
    listen 443 ssl;
    server_name seu-dominio.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🤝 **Contribuindo**

1. **Fork** o projeto
2. **Crie** uma branch (`git checkout -b feature/nova-funcionalidade`)
3. **Commit** suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. **Push** para a branch (`git push origin feature/nova-funcionalidade`)
5. **Abra** um Pull Request

### **Padrões de Código**
- Seguir **PEP 8** para Python
- **ES6+** para JavaScript
- **BEM** para CSS
- **Conventional Commits** para mensagens

---

## 📄 **Licença**

Este projeto está licenciado sob a **MIT License** - veja [LICENSE.md](LICENSE.md) para detalhes.

---

## 👨‍💻 **Autor**

**Luys Fernando**  
🐙 [GitHub](https://github.com/luysfernnando)  
💼 [LinkedIn](https://linkedin.com/in/luysfernnando)  

---

<div align="center">

**⭐ Se este projeto te ajudou, deixe uma estrela!**

*Desenvolvido com ❤️ usando Python, Flask e Clean Architecture*

**🌐 Dashboard Web • 📱 WhatsApp Bot • 📊 Analytics • ⚙️ Configurável**

</div>
