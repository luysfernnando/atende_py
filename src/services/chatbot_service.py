# src/services/chatbot_service.py
"""
Serviço principal do chatbot - Lógica de negócio
Princípio SRP: Apenas lógica de processamento de mensagens
Princípio OCP: Aberto para extensão (novos tipos de fluxo)
"""

from typing import Dict
from ..models.conversa import Conversa, EstadoConversa
from ..models.consulta import Consulta
from ..database.consulta_repository import ConsultaRepository
from ..database.conversa_repository import ConversaRepository
from .ai_service import AIService

class ChatbotService:
    """Serviço principal para processamento de mensagens do chatbot"""
    
    def __init__(self, consulta_repo: ConsultaRepository, conversa_repo: ConversaRepository, ai_service: AIService = None):
        self.consulta_repo = consulta_repo
        self.conversa_repo = conversa_repo
        self.ai_service = ai_service or AIService()
        self._conversas_ativas: Dict[str, Conversa] = {}
    
    def processar_mensagem(self, user_id: str, mensagem: str) -> str:
        """Processa uma mensagem do usuário e retorna a resposta"""
        conversa = self._obter_conversa(user_id)
        
        # Analisa intenção com IA
        intencao = self.ai_service.processar_intencao(mensagem)
        
        # Se a IA tem uma resposta sugerida e não estamos no meio de um fluxo
        if intencao.get('resposta_sugerida') and conversa.estado == EstadoConversa.INICIAL:
            if intencao['intencao'] == 'iniciar_conversa':
                resposta = self._iniciar_conversa(conversa)
            else:
                resposta = intencao['resposta_sugerida']
        else:
            # Processa pelo fluxo normal
            resposta = self._processar_por_estado(conversa, mensagem, intencao)
        
        # Melhora a resposta com IA
        resposta = self.ai_service.melhorar_resposta(resposta, intencao)
        
        # Salva o estado e histórico
        self.conversa_repo.salvar_estado(conversa)
        self.conversa_repo.salvar_historico(user_id, mensagem, resposta, conversa.estado)
        
        return resposta
    
    def _obter_conversa(self, user_id: str) -> Conversa:
        """Obtém ou cria uma conversa para o usuário"""
        if user_id not in self._conversas_ativas:
            # Tenta carregar do banco
            conversa = self.conversa_repo.carregar_estado(user_id)
            if not conversa:
                conversa = Conversa(user_id=user_id)
            self._conversas_ativas[user_id] = conversa
        
        return self._conversas_ativas[user_id]
    
    def _processar_por_estado(self, conversa: Conversa, mensagem: str, intencao: Dict) -> str:
        """Processa a mensagem baseada no estado atual"""
        if conversa.estado == EstadoConversa.INICIAL:
            return self._iniciar_conversa(conversa)
        
        elif conversa.estado == EstadoConversa.AGUARDANDO_NOME:
            return self._processar_nome(conversa, mensagem)
        
        elif conversa.estado == EstadoConversa.AGUARDANDO_DATA:
            return self._processar_data(conversa, mensagem, intencao)
        
        elif conversa.estado == EstadoConversa.AGUARDANDO_PERIODO:
            return self._processar_periodo(conversa, mensagem, intencao)
        
        elif conversa.estado == EstadoConversa.FINALIZADO:
            return self._processar_finalizado(conversa, mensagem)
        
        return "Desculpe, não entendi. Digite 'iniciar' para começar uma nova conversa."
    
    def _iniciar_conversa(self, conversa: Conversa) -> str:
        """Inicia uma nova conversa"""
        conversa.estado = EstadoConversa.AGUARDANDO_NOME
        return "Olá! Vou te ajudar a marcar uma consulta. 😊\n\nQual é o seu nome?"
    
    def _processar_nome(self, conversa: Conversa, nome: str) -> str:
        """Processa o nome do usuário"""
        nome = nome.strip()
        conversa.adicionar_dado('nome', nome)
        conversa.estado = EstadoConversa.AGUARDANDO_DATA
        return f"Muito bem, {nome}! 👍\n\nAgora me diga em que data você gostaria de marcar a consulta? (exemplo: 15/06/2025)"
    
    def _processar_data(self, conversa: Conversa, data: str, intencao: Dict) -> str:
        """Processa a data da consulta"""
        # Tenta extrair data com IA primeiro
        data_extraida = intencao.get('data_extraida')
        if data_extraida:
            data = data_extraida
        else:
            data = data.strip()
        
        conversa.adicionar_dado('data', data)
        conversa.estado = EstadoConversa.AGUARDANDO_PERIODO
        return f"Perfeito! Data: {data} ✅\n\nQual período você prefere?\n• Digite 'manhã' para período da manhã\n• Digite 'tarde' para período da tarde"
    
    def _processar_periodo(self, conversa: Conversa, periodo: str, intencao: Dict) -> str:
        """Processa o período da consulta"""
        # Tenta extrair período com IA primeiro
        entidades = self.ai_service.extrair_entidades(periodo)
        periodo_extraido = entidades.get('periodo')
        
        if periodo_extraido:
            periodo = periodo_extraido
        else:
            periodo = periodo.strip().lower()
            if periodo not in ['manhã', 'manha', 'tarde']:
                return "Por favor, digite apenas 'manhã' ou 'tarde' para o período da consulta."
        
        conversa.adicionar_dado('periodo', periodo)
        conversa.estado = EstadoConversa.FINALIZADO
        
        # Cria e salva a consulta
        consulta = Consulta(
            nome=conversa.dados['nome'],
            data=conversa.dados['data'],
            periodo=periodo,
            user_id=conversa.user_id
        )
        
        consulta_id = self.consulta_repo.salvar(consulta)
        
        resposta = "🎉 Consulta marcada com sucesso!\n\n"
        resposta += "📋 **Resumo da sua consulta:**\n"
        resposta += f"👤 Nome: {conversa.dados['nome']}\n"
        resposta += f"📅 Data: {conversa.dados['data']}\n"
        resposta += f"⏰ Período: {periodo}\n"
        resposta += f"🆔 ID da consulta: {consulta_id}\n\n"
        resposta += "✅ Sua consulta foi registrada no banco de dados! Para marcar uma nova consulta, digite 'nova' ou 'iniciar'."
        
        return resposta
    
    def _processar_finalizado(self, conversa: Conversa, mensagem: str) -> str:
        """Processa mensagens quando a conversa está finalizada"""
        if mensagem.strip().lower() in ['nova', 'iniciar', 'novo', 'começar']:
            conversa.reiniciar()
            return self._iniciar_conversa(conversa)
        
        return "Para marcar uma nova consulta, digite 'nova' ou 'iniciar'. 😊"
    
    def reiniciar_conversa(self, user_id: str):
        """Reinicia a conversa de um usuário"""
        if user_id in self._conversas_ativas:
            self._conversas_ativas[user_id].reiniciar()
        self.conversa_repo.remover_estado(user_id)
    
    def obter_status_conversa(self, user_id: str) -> dict:
        """Obtém o status atual da conversa"""
        conversa = self._obter_conversa(user_id)
        return conversa.to_dict()