# app.py
"""
Aplicação principal do chatbot seguindo princípios SOLID e KISS
- SRP: Cada classe tem uma responsabilidade única
- OCP: Aberto para extensão, fechado para modificação
- LSP: Substituição de Liskov respeitada
- ISP: Interfaces segregadas (repositórios específicos)
- DIP: Dependência de abstrações, não implementações
"""

import os
from dotenv import load_dotenv
from flask import Flask, render_template, send_from_directory
from src.database.database_manager import DatabaseManager
from src.database.consulta_repository import ConsultaRepository
from src.database.conversa_repository import ConversaRepository
from src.services.chatbot_service import ChatbotService
from src.services.ai_service import AIService
from src.services.whatsapp_service import WhatsAppService
from src.controllers.chatbot_controller import ChatbotController
from src.controllers.whatsapp_controller import WhatsAppController

# Carrega variáveis de ambiente
load_dotenv()

def create_app() -> Flask:
    """Factory pattern para criar a aplicação Flask"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # Configuração das dependências (Dependency Injection)
    db_manager = DatabaseManager()
    consulta_repo = ConsultaRepository(db_manager)
    conversa_repo = ConversaRepository(db_manager)
    ai_service = AIService()
    chatbot_service = ChatbotService(consulta_repo, conversa_repo, ai_service)
    
    # Controllers
    chatbot_controller = ChatbotController(chatbot_service, consulta_repo, conversa_repo)
    
    # WhatsApp service e controller (opcional, só se configurado)
    whatsapp_controller = None
    try:
        whatsapp_service = WhatsAppService()
        whatsapp_controller = WhatsAppController(whatsapp_service, chatbot_service)
        print("✅ WhatsApp integrado com sucesso!")
    except ValueError as e:
        print(f"⚠️  WhatsApp não configurado: {e}")
        print("💡 Configure as variáveis do Twilio no arquivo .env para usar WhatsApp")
    
    # Registra as rotas
    register_routes(app, chatbot_controller, whatsapp_controller)
    
    return app

def register_routes(app: Flask, chatbot_controller: ChatbotController, whatsapp_controller: WhatsAppController = None):
    """Registra todas as rotas da aplicação"""
    
    # Rota para o dashboard web
    @app.route('/')
    def dashboard():
        return render_template('dashboard.html')
    
    @app.route('/static/<path:filename>')
    def static_files(filename):
        return send_from_directory('static', filename)
    
    # Rotas do chatbot (API REST)
    @app.route('/mensagem', methods=['POST'])
    def mensagem():
        return chatbot_controller.processar_mensagem()
    
    @app.route('/consultas', methods=['GET'])
    def listar_consultas():
        return chatbot_controller.listar_consultas()
    
    @app.route('/consultas/<user_id>', methods=['GET'])
    def consultas_usuario(user_id: str):
        return chatbot_controller.consultas_usuario(user_id)
    
    @app.route('/historico/<user_id>', methods=['GET'])
    def historico_conversa(user_id: str):
        return chatbot_controller.historico_conversa(user_id)
    
    @app.route('/conversa/status/<user_id>', methods=['GET'])
    def status_conversa(user_id: str):
        return chatbot_controller.status_conversa(user_id)
    
    @app.route('/conversa/reiniciar/<user_id>', methods=['POST'])
    def reiniciar_conversa(user_id: str):
        return chatbot_controller.reiniciar_conversa(user_id)
    
    @app.route('/estatisticas', methods=['GET'])
    def estatisticas():
        return chatbot_controller.estatisticas()
    
    @app.route('/health', methods=['GET'])
    def health_check():
        return {'status': 'ok', 'message': 'Chatbot funcionando!'}
    
    # Nova rota para fornecer configurações do .env
    @app.route('/config', methods=['GET'])
    def get_config():
        """Retorna configurações atuais (sem dados sensíveis)"""
        return {
            'twilio_sid': os.getenv('TWILIO_ACCOUNT_SID', ''),
            'whatsapp_number': os.getenv('TWILIO_PHONE_NUMBER', ''),
            'has_token': bool(os.getenv('TWILIO_AUTH_TOKEN'))
        }
    
    # Rotas do WhatsApp (se configurado)
    if whatsapp_controller:
        @app.route('/webhook/whatsapp', methods=['POST'])
        def webhook_whatsapp():
            return whatsapp_controller.webhook_whatsapp()
        
        @app.route('/whatsapp/enviar', methods=['POST'])
        def enviar_whatsapp():
            return whatsapp_controller.enviar_mensagem_direta()

if __name__ == '__main__':
    app = create_app()
    print("💾 Banco de dados SQLite inicializado!")
    print("🤖 IA leve integrada!")
    print("🚀 Servidor iniciado em: http://localhost:5000")
    print("\n📋 Endpoints disponíveis:")
    print("• POST /mensagem - Enviar mensagem para o chatbot")
    print("• GET /consultas - Listar todas as consultas")
    print("• GET /consultas/<user_id> - Consultas de um usuário")
    print("• GET /historico/<user_id> - Histórico de conversa")
    print("• GET /conversa/status/<user_id> - Status da conversa")
    print("• POST /conversa/reiniciar/<user_id> - Reiniciar conversa")
    print("• GET /estatisticas - Estatísticas do sistema")
    print("• GET /health - Health check")
    print("• GET /config - Obter configurações atuais")
    
    # Mostra endpoints do WhatsApp se configurado
    if os.getenv('TWILIO_ACCOUNT_SID'):
        print("\n📱 Endpoints WhatsApp:")
        print("• POST /webhook/whatsapp - Webhook para Twilio")
        print("• POST /whatsapp/enviar - Enviar mensagem direta")
    
    app.run(debug=True, host='0.0.0.0', port=5000)