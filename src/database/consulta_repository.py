# src/database/consulta_repository.py
"""
Repository para operações com consultas
Princípio SRP: Apenas operações de consulta no banco
Princípio DIP: Depende de abstração (DatabaseManager)
"""

import json
from typing import List, Optional
from ..models.consulta import Consulta
from .database_manager import DatabaseManager

class ConsultaRepository:
    """Repository para operações com consultas"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def salvar(self, consulta: Consulta) -> int:
        """Salva uma consulta e retorna o ID"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO consultas (nome, data, periodo, user_id)
            VALUES (?, ?, ?, ?)
        ''', (consulta.nome, consulta.data, consulta.periodo, consulta.user_id))
        
        consulta_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return consulta_id
    
    def buscar_todas(self) -> List[Consulta]:
        """Busca todas as consultas"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, nome, data, periodo, data_criacao, user_id 
            FROM consultas 
            ORDER BY data_criacao DESC
        ''')
        
        consultas = []
        for row in cursor.fetchall():
            consulta = Consulta(
                id=row[0],
                nome=row[1],
                data=row[2],
                periodo=row[3],
                data_criacao=row[4],
                user_id=row[5]
            )
            consultas.append(consulta)
        
        conn.close()
        return consultas
    
    def buscar_por_usuario(self, user_id: str) -> List[Consulta]:
        """Busca consultas de um usuário específico"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, nome, data, periodo, data_criacao, user_id
            FROM consultas 
            WHERE user_id = ?
            ORDER BY data_criacao DESC
        ''', (user_id,))
        
        consultas = []
        for row in cursor.fetchall():
            consulta = Consulta(
                id=row[0],
                nome=row[1],
                data=row[2],
                periodo=row[3],
                data_criacao=row[4],
                user_id=row[5]
            )
            consultas.append(consulta)
        
        conn.close()
        return consultas
    
    def obter_estatisticas(self) -> dict:
        """Obtém estatísticas das consultas"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        # Total de consultas
        cursor.execute('SELECT COUNT(*) FROM consultas')
        total_consultas = cursor.fetchone()[0]
        
        # Consultas por período
        cursor.execute('SELECT periodo, COUNT(*) FROM consultas GROUP BY periodo')
        por_periodo = dict(cursor.fetchall())
        
        # Usuários únicos
        cursor.execute('SELECT COUNT(DISTINCT user_id) FROM consultas')
        usuarios_unicos = cursor.fetchone()[0]
        
        # Últimas consultas
        cursor.execute('''
            SELECT nome, data, periodo, data_criacao 
            FROM consultas 
            ORDER BY data_criacao DESC 
            LIMIT 5
        ''')
        
        ultimas_consultas = []
        for row in cursor.fetchall():
            ultimas_consultas.append({
                'nome': row[0],
                'data': row[1],
                'periodo': row[2],
                'data_criacao': row[3]
            })
        
        conn.close()
        
        return {
            'total_consultas': total_consultas,
            'consultas_por_periodo': por_periodo,
            'usuarios_unicos': usuarios_unicos,
            'ultimas_consultas': ultimas_consultas
        }