# src/models/consulta.py
"""
Modelo de dados para Consulta
Princípio SRP (Single Responsibility): Apenas dados da consulta
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class Consulta:
    """Modelo de dados para uma consulta médica"""
    nome: str
    data: str
    periodo: str
    user_id: str
    id: Optional[int] = None
    data_criacao: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'data': self.data,
            'periodo': self.periodo,
            'user_id': self.user_id,
            'data_criacao': self.data_criacao
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Consulta':
        """Cria uma instância a partir de um dicionário"""
        return cls(
            id=data.get('id'),
            nome=data['nome'],
            data=data['data'],
            periodo=data['periodo'],
            user_id=data['user_id'],
            data_criacao=data.get('data_criacao')
        )