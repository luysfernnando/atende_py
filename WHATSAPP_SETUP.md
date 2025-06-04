# 📱 Guia de Configuração WhatsApp + IA

Este guia explica como configurar a integração com WhatsApp via Twilio e usar as funcionalidades de IA.

## 🔧 Configuração do WhatsApp (Twilio)

### 1. Criar conta no Twilio
1. Acesse [twilio.com](https://www.twilio.com)
2. Crie uma conta gratuita
3. Vá para o Console do Twilio

### 2. Configurar WhatsApp Sandbox
1. No Console, vá para **Develop > Messaging > Try it out > Send a WhatsApp message**
2. Siga as instruções para configurar o Sandbox
3. Anote o número do Sandbox (ex: +1 415 523 8886)

### 3. Obter credenciais
No Console do Twilio, copie:
- **Account SID**
- **Auth Token**
- **Número do WhatsApp** (do Sandbox)

### 4. Configurar variáveis de ambiente
Copie o arquivo `.env.example` para `.env`:
```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:
```bash
# Configurações do Twilio
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=+14155238886

# Configurações da aplicação
FLASK_ENV=development
SECRET_KEY=minha-chave-secreta-123

# URL base para webhooks (substitua pela sua URL do ngrok)
BASE_URL=https://abc123.ngrok.io
```

### 5. Configurar webhook no Twilio
1. Instale o ngrok: `npm install -g ngrok` ou baixe em [ngrok.com](https://ngrok.com)
2. Execute o ngrok: `ngrok http 5000`
3. Copie a URL HTTPS gerada (ex: `https://abc123.ngrok.io`)
4. No Console do Twilio, vá para WhatsApp Sandbox Settings
5. Cole a URL do webhook: `https://abc123.ngrok.io/webhook/whatsapp`

## 🚀 Como usar

### 1. Instalar dependências
```bash
# Ativar ambiente virtual
source chatbotenv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Executar aplicação
```bash
python app.py
```

### 3. Testar via WhatsApp
1. Envie a mensagem de ativação para o número do Sandbox (conforme instruções do Twilio)
2. Converse normalmente com o chatbot
3. Exemplos de mensagens:
   - "Oi" ou "Olá" → Saudação
   - "Iniciar" → Começar nova consulta
   - "Ajuda" → Menu de ajuda
   - "15/06/2025" → Data será detectada automaticamente
   - "manhã" ou "tarde" → Período será detectado

## 🤖 Funcionalidades de IA

### Detecção de Intenções
- **Saudações**: Oi, olá, bom dia, etc.
- **Despedidas**: Tchau, obrigado, até logo, etc.
- **Iniciar conversa**: Iniciar, nova, marcar, agendar, etc.
- **Ajuda**: Ajuda, help, como, etc.

### Extração de Entidades
- **Datas**: Detecta formatos dd/mm/aaaa, dd-mm-aaaa, dd.mm.aaaa
- **Períodos**: Detecta "manhã", "tarde" em textos livres
- **Normalização**: Remove acentos e normaliza texto

### Melhorias na Conversa
- Adiciona emojis apropriados
- Respostas mais naturais
- Detecção automática de dados
- Mensagens de ajuda contextuais

## 🧪 Testando a API

### Teste básico (sem WhatsApp)
```bash
curl -X POST http://localhost:5000/mensagem \
  -H "Content-Type: application/json" \
  -d '{"user_id": "teste", "mensagem": "Oi"}'
```

### Teste de data automática
```bash
curl -X POST http://localhost:5000/mensagem \
  -H "Content-Type: application/json" \
  -d '{"user_id": "teste", "mensagem": "Quero marcar para 15/06/2025"}'
```

### Enviar WhatsApp direto (se configurado)
```bash
curl -X POST http://localhost:5000/whatsapp/enviar \
  -H "Content-Type: application/json" \
  -d '{"numero": "+5511999999999", "mensagem": "Teste do chatbot!"}'
```

## 🏗️ Arquitetura (Princípios SOLID)

### Single Responsibility Principle (SRP)
- `WhatsAppService`: Apenas comunicação com Twilio
- `AIService`: Apenas processamento de IA
- `ChatbotService`: Apenas lógica de negócio
- `WhatsAppController`: Apenas controle de requisições WhatsApp

### Open/Closed Principle (OCP)
- Fácil adicionar novos tipos de IA (ChatterBot, OpenAI, etc.)
- Fácil adicionar novos canais (Telegram, Discord, etc.)

### Dependency Inversion Principle (DIP)
- Controllers dependem de Services (abstrações)
- Services podem ser facilmente substituídos

## 🔍 Logs e Debug

O sistema imprime logs úteis:
```
✅ WhatsApp integrado com sucesso!
🤖 IA leve integrada!
💾 Banco de dados SQLite inicializado!
```

Se o WhatsApp não estiver configurado:
```
⚠️  WhatsApp não configurado: Configurações do Twilio não encontradas
💡 Configure as variáveis do Twilio no arquivo .env para usar WhatsApp
```

## 🚨 Troubleshooting

### Erro: "Configurações do Twilio não encontradas"
- Verifique se o arquivo `.env` existe
- Verifique se as variáveis estão corretas
- Reinicie a aplicação

### Webhook não funciona
- Verifique se o ngrok está rodando
- Verifique se a URL no Twilio está correta
- Verifique se o endpoint `/webhook/whatsapp` está acessível

### IA não detecta intenções
- Verifique se as mensagens estão em português
- A IA é sensível a acentos (mas os normaliza)
- Teste com palavras exatas: "oi", "iniciar", "ajuda"

## 🔄 Próximos passos

Para expandir ainda mais:
1. **OpenAI**: Integrar GPT para respostas mais inteligentes
2. **Telegram**: Adicionar suporte a Telegram  
3. **Spacy/NLTK**: Para processamento de linguagem natural avançado
4. **Validações**: Adicionar validação de datas e horários mais robusta
5. **Notificações**: Enviar lembretes de consultas
6. **Machine Learning**: Treinar modelos personalizados com histórico de conversas