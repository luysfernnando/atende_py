# src/services/whatsapp_service.py
"""
Serviço para integração com WhatsApp via Twilio
Princípio SRP: Apenas responsável pela comunicação com WhatsApp
Princípio DIP: Depende de abstrações (interfaces)
"""

import os
from typing import Optional
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse


class WhatsAppService:
    """Serviço para envio e recebimento de mensagens WhatsApp via Twilio"""
    
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.phone_number = os.getenv('TWILIO_PHONE_NUMBER')
        
        if not all([self.account_sid, self.auth_token, self.phone_number]):
            raise ValueError("Configurações do Twilio não encontradas nas variáveis de ambiente")
        
        self.client = Client(self.account_sid, self.auth_token)
    
    def enviar_mensagem(self, para: str, mensagem: str) -> Optional[str]:
        """
        Envia uma mensagem via WhatsApp
        
        Args:
            para: Número do destinatário (formato: whatsapp:+5511999999999)
            mensagem: Texto da mensagem
            
        Returns:
            SID da mensagem se enviada com sucesso, None caso contrário
        """
        try:
            if not para.startswith('whatsapp:'):
                para = f'whatsapp:{para}'
            
            message = self.client.messages.create(
                body=mensagem,
                from_=f'whatsapp:{self.phone_number}',
                to=para
            )
            
            return message.sid
            
        except Exception as e:
            print(f"Erro ao enviar mensagem WhatsApp: {e}")
            return None
    
    def criar_resposta_webhook(self, mensagem: str) -> str:
        """
        Cria uma resposta TwiML para webhook do Twilio
        
        Args:
            mensagem: Mensagem de resposta
            
        Returns:
            String XML da resposta TwiML
        """
        response = MessagingResponse()
        response.message(mensagem)
        return str(response)
    
    def extrair_dados_webhook(self, request_form) -> dict:
        """
        Extrai dados do webhook do Twilio
        
        Args:
            request_form: Form data da requisição Flask
            
        Returns:
            Dicionário com os dados extraídos
        """
        return {
            'from': request_form.get('From', ''),
            'to': request_form.get('To', ''),
            'body': request_form.get('Body', ''),
            'message_sid': request_form.get('MessageSid', ''),
            'num_media': request_form.get('NumMedia', '0')
        }