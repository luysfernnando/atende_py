# tests/test_models.py
"""
Testes unitários para os modelos de dados
Testa a lógica dos modelos isoladamente
"""

import unittest
from src.models.consulta import Consulta
from src.models.conversa import Conversa, EstadoConversa

class TestConsulta(unittest.TestCase):
    """Testes para o modelo Consulta"""
    
    def test_criacao_consulta(self):
        """Testa a criação de uma consulta"""
        consulta = Consulta(
            nome="João Silva",
            data="15/06/2025",
            periodo="manhã",
            user_id="user123"
        )
        
        self.assertEqual(consulta.nome, "João Silva")
        self.assertEqual(consulta.data, "15/06/2025")
        self.assertEqual(consulta.periodo, "manhã")
        self.assertEqual(consulta.user_id, "user123")
        self.assertIsNone(consulta.id)
    
    def test_to_dict(self):
        """Testa a conversão para dicionário"""
        consulta = Consulta(
            nome="Maria Costa",
            data="20/06/2025",
            periodo="tarde",
            user_id="user456",
            id=1
        )
        
        expected = {
            'id': 1,
            'nome': 'Maria Costa',
            'data': '20/06/2025',
            'periodo': 'tarde',
            'user_id': 'user456',
            'data_criacao': None
        }
        
        self.assertEqual(consulta.to_dict(), expected)
    
    def test_from_dict(self):
        """Testa a criação a partir de dicionário"""
        data = {
            'id': 2,
            'nome': 'Pedro Santos',
            'data': '25/06/2025',
            'periodo': 'manhã',
            'user_id': 'user789'
        }
        
        consulta = Consulta.from_dict(data)
        
        self.assertEqual(consulta.id, 2)
        self.assertEqual(consulta.nome, 'Pedro Santos')
        self.assertEqual(consulta.user_id, 'user789')

class TestConversa(unittest.TestCase):
    """Testes para o modelo Conversa"""
    
    def test_criacao_conversa(self):
        """Testa a criação de uma conversa"""
        conversa = Conversa(user_id="user123")
        
        self.assertEqual(conversa.user_id, "user123")
        self.assertEqual(conversa.estado, EstadoConversa.INICIAL)
        self.assertEqual(conversa.dados, {})
    
    def test_adicionar_dado(self):
        """Testa adicionar dados à conversa"""
        conversa = Conversa(user_id="user123")
        conversa.adicionar_dado("nome", "João")
        
        self.assertEqual(conversa.dados["nome"], "João")
    
    def test_tem_todos_dados(self):
        """Testa verificação de dados completos"""
        conversa = Conversa(user_id="user123")
        
        self.assertFalse(conversa.tem_todos_dados())
        
        conversa.adicionar_dado("nome", "João")
        conversa.adicionar_dado("data", "15/06/2025")
        self.assertFalse(conversa.tem_todos_dados())
        
        conversa.adicionar_dado("periodo", "manhã")
        self.assertTrue(conversa.tem_todos_dados())
    
    def test_reiniciar_conversa(self):
        """Testa reinicialização da conversa"""
        conversa = Conversa(user_id="user123")
        conversa.estado = EstadoConversa.FINALIZADO
        conversa.adicionar_dado("nome", "João")
        
        conversa.reiniciar()
        
        self.assertEqual(conversa.estado, EstadoConversa.INICIAL)
        self.assertEqual(conversa.dados, {})
    
    def test_to_dict(self):
        """Testa conversão para dicionário"""
        conversa = Conversa(user_id="user123")
        conversa.estado = EstadoConversa.AGUARDANDO_NOME
        conversa.adicionar_dado("teste", "valor")
        
        result = conversa.to_dict()
        
        self.assertEqual(result['user_id'], "user123")
        self.assertEqual(result['estado'], "aguardando_nome")
        self.assertEqual(result['dados'], {"teste": "valor"})

if __name__ == '__main__':
    unittest.main()