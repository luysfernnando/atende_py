# src/database/database_manager.py
"""
Gerenciador de banco de dados SQLite
Princípio SRP: Apenas configuração e inicialização do banco
"""

import sqlite3
from typing import Optional

class DatabaseManager:
    """Gerencia conexões e inicialização do banco SQLite"""
    
    def __init__(self, database_path: str = 'chatbot.db'):
        self.database_path = database_path
        self.init_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """Retorna uma nova conexão com o banco"""
        return sqlite3.connect(self.database_path)
    
    def init_database(self):
        """Inicializa as tabelas do banco de dados"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabela para consultas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS consultas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                data TEXT NOT NULL,
                periodo TEXT NOT NULL,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_id TEXT
            )
        ''')
        
        # Tabela para histórico de conversas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historico_conversas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                mensagem_usuario TEXT,
                resposta_bot TEXT,
                estado TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela para estado das conversas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS estados_conversa (
                user_id TEXT PRIMARY KEY,
                estado TEXT NOT NULL,
                dados_coletados TEXT,
                ultima_atividade TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()