# src/controllers/chatbot_controller.py
"""
Controller para endpoints do chatbot
Princípio SRP: Apenas controle de requisições HTTP
Princípio DIP: Depende de abstrações (services)
"""

from flask import request, jsonify
from ..services.chatbot_service import ChatbotService
from ..database.consulta_repository import ConsultaRepository
from ..database.conversa_repository import ConversaRepository

class ChatbotController:
    """Controller para gerenciar as rotas do chatbot"""
    
    def __init__(self, chatbot_service: ChatbotService, consulta_repo: ConsultaRepository, conversa_repo: ConversaRepository):
        self.chatbot_service = chatbot_service
        self.consulta_repo = consulta_repo
        self.conversa_repo = conversa_repo
    
    def processar_mensagem(self):
        """Endpoint para processar mensagens do usuário"""
        try:
            dados = request.json
            user_id = dados.get('user_id', 'default')
            mensagem_usuario = dados.get('mensagem', '')
            
            if not mensagem_usuario.strip():
                return jsonify({'erro': 'Mensagem não pode estar vazia'}), 400
            
            resposta = self.chatbot_service.processar_mensagem(user_id, mensagem_usuario)
            status = self.chatbot_service.obter_status_conversa(user_id)
            
            return jsonify({
                'resposta': resposta,
                'user_id': user_id,
                'estado': status['estado']
            })
            
        except Exception as e:
            return jsonify({'erro': f'Erro interno: {str(e)}'}), 500
    
    def listar_consultas(self):
        """Endpoint para listar todas as consultas"""
        try:
            consultas = self.consulta_repo.buscar_todas()
            return jsonify([consulta.to_dict() for consulta in consultas])
        except Exception as e:
            return jsonify({'erro': f'Erro ao buscar consultas: {str(e)}'}), 500
    
    def consultas_usuario(self, user_id: str):
        """Endpoint para listar consultas de um usuário"""
        try:
            consultas = self.consulta_repo.buscar_por_usuario(user_id)
            return jsonify([consulta.to_dict() for consulta in consultas])
        except Exception as e:
            return jsonify({'erro': f'Erro ao buscar consultas do usuário: {str(e)}'}), 500
    
    def historico_conversa(self, user_id: str):
        """Endpoint para obter histórico de conversa"""
        try:
            historico = self.conversa_repo.buscar_historico(user_id)
            return jsonify(historico)
        except Exception as e:
            return jsonify({'erro': f'Erro ao buscar histórico: {str(e)}'}), 500
    
    def status_conversa(self, user_id: str):
        """Endpoint para verificar status da conversa"""
        try:
            status = self.chatbot_service.obter_status_conversa(user_id)
            return jsonify(status)
        except Exception as e:
            return jsonify({'erro': f'Erro ao obter status: {str(e)}'}), 500
    
    def reiniciar_conversa(self, user_id: str):
        """Endpoint para reiniciar conversa"""
        try:
            self.chatbot_service.reiniciar_conversa(user_id)
            return jsonify({'mensagem': 'Conversa reiniciada com sucesso!'})
        except Exception as e:
            return jsonify({'erro': f'Erro ao reiniciar conversa: {str(e)}'}), 500
    
    def estatisticas(self):
        """Endpoint para obter estatísticas do sistema"""
        try:
            stats = self.consulta_repo.obter_estatisticas()
            return jsonify(stats)
        except Exception as e:
            return jsonify({'erro': f'Erro ao obter estatísticas: {str(e)}'}), 500