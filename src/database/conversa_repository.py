# src/database/conversa_repository.py
"""
Repository para operações com conversas e histórico
Princípio SRP: Apenas operações de conversa no banco
"""

import json
from typing import List, Optional
from ..models.conversa import Conversa, EstadoConversa
from .database_manager import DatabaseManager

class ConversaRepository:
    """Repository para operações com estado de conversas e histórico"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def salvar_estado(self, conversa: Conversa):
        """Salva o estado atual da conversa"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        dados_json = json.dumps(conversa.dados)
        
        cursor.execute('''
            INSERT OR REPLACE INTO estados_conversa (user_id, estado, dados_coletados)
            VALUES (?, ?, ?)
        ''', (conversa.user_id, conversa.estado.value, dados_json))
        
        conn.commit()
        conn.close()
    
    def carregar_estado(self, user_id: str) -> Optional[Conversa]:
        """Carrega o estado da conversa do banco"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT estado, dados_coletados FROM estados_conversa WHERE user_id = ?
        ''', (user_id,))
        
        resultado = cursor.fetchone()
        conn.close()
        
        if resultado:
            estado_str, dados_json = resultado
            dados = json.loads(dados_json) if dados_json else {}
            estado = EstadoConversa(estado_str)
            
            return Conversa(
                user_id=user_id,
                estado=estado,
                dados=dados
            )
        
        return None
    
    def remover_estado(self, user_id: str):
        """Remove o estado da conversa"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM estados_conversa WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()
    
    def salvar_historico(self, user_id: str, mensagem_usuario: str, resposta_bot: str, estado: EstadoConversa):
        """Salva uma interação no histórico"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO historico_conversas (user_id, mensagem_usuario, resposta_bot, estado)
            VALUES (?, ?, ?, ?)
        ''', (user_id, mensagem_usuario, resposta_bot, estado.value))
        
        conn.commit()
        conn.close()
    
    def buscar_historico(self, user_id: str) -> List[dict]:
        """Busca o histórico de conversas de um usuário"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT mensagem_usuario, resposta_bot, estado, timestamp 
            FROM historico_conversas 
            WHERE user_id = ?
            ORDER BY timestamp ASC
        ''', (user_id,))
        
        historico = []
        for row in cursor.fetchall():
            historico.append({
                'mensagem_usuario': row[0],
                'resposta_bot': row[1],
                'estado': row[2],
                'timestamp': row[3]
            })
        
        conn.close()
        return historico