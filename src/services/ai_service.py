# src/services/ai_service.py
"""
Serviço de IA leve para processamento de linguagem natural
Princípio SRP: Apenas responsável pelo processamento de IA
Princípio OCP: Aberto para extensão (diferentes engines de IA)
"""

import re
from typing import Dict, List


class AIService:
    """Serviço de IA leve para melhorar a interação do chatbot"""
    
    def __init__(self):
        self.saudacoes = [
            'oi', 'olá', 'ola', 'hey', 'ei', 'bom dia', 'boa tarde', 'boa noite'
        ]
        
        self.despedidas = [
            'tchau', 'bye', 'até logo', 'adeus', 'falou', 'obrigado', 'obrigada'
        ]
        
        self.palavras_iniciar = [
            'iniciar', 'começar', 'comecar', 'nova', 'novo', 'marcar', 'agendar'
        ]
        
        self.palavras_ajuda = [
            'ajuda', 'help', 'socorro', 'como', 'que', 'o que'
        ]
    
    def processar_intencao(self, mensagem: str) -> Dict[str, any]:
        """
        Analisa a intenção do usuário na mensagem
        
        Args:
            mensagem: Texto da mensagem do usuário
            
        Returns:
            Dicionário com a intenção detectada e confiança
        """
        mensagem_limpa = self._limpar_texto(mensagem)
        palavras = mensagem_limpa.split()
        
        # Detecta saudações
        if self._contem_palavras(palavras, self.saudacoes):
            return {
                'intencao': 'saudacao',
                'confianca': 0.8,
                'resposta_sugerida': 'Olá! Como posso ajudar você hoje? 😊'
            }
        
        # Detecta despedidas
        if self._contem_palavras(palavras, self.despedidas):
            return {
                'intencao': 'despedida',
                'confianca': 0.8,
                'resposta_sugerida': 'Até logo! Foi um prazer ajudar você! 👋'
            }
        
        # Detecta intenção de iniciar conversa
        if self._contem_palavras(palavras, self.palavras_iniciar):
            return {
                'intencao': 'iniciar_conversa',
                'confianca': 0.9,
                'resposta_sugerida': None  # Será processado pelo fluxo normal
            }
        
        # Detecta pedidos de ajuda
        if self._contem_palavras(palavras, self.palavras_ajuda):
            return {
                'intencao': 'ajuda',
                'confianca': 0.7,
                'resposta_sugerida': self._gerar_ajuda()
            }
        
        # Detecta datas
        data_detectada = self._detectar_data(mensagem)
        if data_detectada:
            return {
                'intencao': 'data',
                'confianca': 0.85,
                'data_extraida': data_detectada,
                'resposta_sugerida': None
            }
        
        return {
            'intencao': 'desconhecida',
            'confianca': 0.3,
            'resposta_sugerida': None
        }
    
    def melhorar_resposta(self, resposta_original: str, intencao: Dict) -> str:
        """
        Melhora a resposta original baseada na intenção detectada
        
        Args:
            resposta_original: Resposta original do chatbot
            intencao: Dicionário com a intenção detectada
            
        Returns:
            Resposta melhorada
        """
        if intencao.get('resposta_sugerida'):
            return intencao['resposta_sugerida']
        
        # Adiciona emojis e torna mais natural
        resposta = resposta_original
        
        if 'nome' in resposta.lower():
            resposta = resposta.replace('nome?', 'nome? 😊')
        
        if 'data' in resposta.lower():
            resposta = resposta.replace('data?', 'data? 📅')
        
        if 'período' in resposta.lower() or 'periodo' in resposta.lower():
            resposta = resposta.replace('período?', 'período? ⏰')
        
        return resposta
    
    def extrair_entidades(self, mensagem: str) -> Dict[str, str]:
        """
        Extrai entidades da mensagem (nome, data, período)
        
        Args:
            mensagem: Texto da mensagem
            
        Returns:
            Dicionário com entidades extraídas
        """
        entidades = {}
        
        # Extrai possível data
        data = self._detectar_data(mensagem)
        if data:
            entidades['data'] = data
        
        # Extrai período
        periodo = self._detectar_periodo(mensagem)
        if periodo:
            entidades['periodo'] = periodo
        
        return entidades
    
    def _limpar_texto(self, texto: str) -> str:
        """Remove acentos e normaliza texto"""
        texto = texto.lower().strip()
        # Substitui acentos comuns
        acentos = {
            'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a',
            'é': 'e', 'ê': 'e',
            'í': 'i', 'î': 'i',
            'ó': 'o', 'ô': 'o', 'õ': 'o',
            'ú': 'u', 'û': 'u',
            'ç': 'c'
        }
        for acento, letra in acentos.items():
            texto = texto.replace(acento, letra)
        return texto
    
    def _contem_palavras(self, palavras: List[str], lista_palavras: List[str]) -> bool:
        """Verifica se alguma palavra da lista está presente"""
        return any(palavra in lista_palavras for palavra in palavras)
    
    def _detectar_data(self, texto: str) -> str:
        """Detecta datas no formato dd/mm/aaaa ou similar"""
        padroes_data = [
            r'\d{1,2}/\d{1,2}/\d{4}',  # dd/mm/aaaa
            r'\d{1,2}-\d{1,2}-\d{4}',  # dd-mm-aaaa
            r'\d{1,2}\.\d{1,2}\.\d{4}' # dd.mm.aaaa
        ]
        
        for padrao in padroes_data:
            match = re.search(padrao, texto)
            if match:
                return match.group()
        
        return None
    
    def _detectar_periodo(self, texto: str) -> str:
        """Detecta período (manhã/tarde) no texto"""
        texto_limpo = self._limpar_texto(texto)
        
        if any(palavra in texto_limpo for palavra in ['manha', 'manhã']):
            return 'manhã'
        elif 'tarde' in texto_limpo:
            return 'tarde'
        
        return None
    
    def _gerar_ajuda(self) -> str:
        """Gera texto de ajuda"""
        return """🤖 **Como posso ajudar você:**

📝 **Para marcar uma consulta:**
• Digite 'iniciar' ou 'nova consulta'
• Informe seu nome quando solicitado
• Escolha a data (formato: dd/mm/aaaa)
• Escolha o período (manhã ou tarde)

🔄 **Comandos úteis:**
• 'nova' ou 'iniciar' - Nova consulta
• 'ajuda' - Este menu de ajuda

💡 **Dica:** Seja claro nas suas respostas para um melhor atendimento!"""