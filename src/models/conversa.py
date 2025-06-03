# src/models/conversa.py
"""
Modelo de dados para estado da conversa
Princípio SRP: Apenas gerencia estado da conversa
"""

from dataclasses import dataclass
from typing import Dict, Any
from enum import Enum

class EstadoConversa(Enum):
    """Estados possíveis da conversa"""
    INICIAL = 'inicial'
    AGUARDANDO_NOME = 'aguardando_nome'
    AGUARDANDO_DATA = 'aguardando_data'
    AGUARDANDO_PERIODO = 'aguardando_periodo'
    FINALIZADO = 'finalizado'

@dataclass
class Conversa:
    """Modelo para o estado da conversa de um usuário"""
    user_id: str
    estado: EstadoConversa = EstadoConversa.INICIAL
    dados: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.dados is None:
            self.dados = {}
    
    def reiniciar(self):
        """Reinicia a conversa"""
        self.estado = EstadoConversa.INICIAL
        self.dados = {}
    
    def adicionar_dado(self, chave: str, valor: str):
        """Adiciona um dado coletado"""
        self.dados[chave] = valor
    
    def tem_todos_dados(self) -> bool:
        """Verifica se todos os dados necessários foram coletados"""
        campos_obrigatorios = ['nome', 'data', 'periodo']
        return all(campo in self.dados for campo in campos_obrigatorios)
    
    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            'user_id': self.user_id,
            'estado': self.estado.value,
            'dados': self.dados
        }