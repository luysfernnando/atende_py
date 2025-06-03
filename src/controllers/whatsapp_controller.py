# src/controllers/whatsapp_controller.py
"""
Controller para integração com WhatsApp via Twilio
Princípio SRP: Apenas responsável por requisições do WhatsApp
Princípio DIP: Depende de abstrações (services)
"""

from flask import request
from ..services.whatsapp_service import WhatsAppService
from ..services.chatbot_service import ChatbotService


class WhatsAppController:
    """Controller para gerenciar webhooks do WhatsApp via Twilio"""
    
    def __init__(self, whatsapp_service: WhatsAppService, chatbot_service: ChatbotService):
        self.whatsapp_service = whatsapp_service
        self.chatbot_service = chatbot_service
    
    def webhook_whatsapp(self):
        """Endpoint para receber mensagens do WhatsApp via Twilio"""
        try:
            # Extrai dados do webhook
            dados = self.whatsapp_service.extrair_dados_webhook(request.form)
            
            numero_usuario = dados['from']
            mensagem_usuario = dados['body']
            
            if not mensagem_usuario.strip():
                return self.whatsapp_service.criar_resposta_webhook(
                    "Desculpe, não recebi nenhuma mensagem. Tente novamente."
                )
            
            # Usa o número como user_id (remove whatsapp: prefix)
            user_id = numero_usuario.replace('whatsapp:', '')
            
            # Processa a mensagem com o chatbot
            resposta = self.chatbot_service.processar_mensagem(user_id, mensagem_usuario)
            
            # Retorna resposta TwiML
            return self.whatsapp_service.criar_resposta_webhook(resposta)
            
        except Exception as e:
            print(f"Erro no webhook WhatsApp: {e}")
            return self.whatsapp_service.criar_resposta_webhook(
                "Desculpe, ocorreu um erro interno. Tente novamente mais tarde."
            )
    
    def enviar_mensagem_direta(self):
        """Endpoint para enviar mensagens diretas via WhatsApp (para testes)"""
        try:
            dados = request.json
            numero = dados.get('numero', '')
            mensagem = dados.get('mensagem', '')
            
            if not numero or not mensagem:
                return {'erro': 'Número e mensagem são obrigatórios'}, 400
            
            message_sid = self.whatsapp_service.enviar_mensagem(numero, mensagem)
            
            if message_sid:
                return {'sucesso': True, 'message_sid': message_sid}
            else:
                return {'erro': 'Falha ao enviar mensagem'}, 500
                
        except Exception as e:
            return {'erro': f'Erro interno: {str(e)}'}, 500