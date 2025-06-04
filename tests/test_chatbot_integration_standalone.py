# tests/test_chatbot_integration_standalone.py
"""
Testes de integração standalone que iniciam seu próprio servidor
Ideal para CI/CD onde precisamos de controle total sobre o ambiente
"""

import requests
import unittest
import threading
import time
import sys
import os

# Adiciona o diretório pai ao path para importar o app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

BASE_URL = "http://localhost:5001"

class TestChatbotIntegrationStandalone(unittest.TestCase):
    """Testes de integração que iniciam seu próprio servidor Flask"""
    
    @classmethod
    def setUpClass(cls):
        """Inicia o servidor Flask em uma thread separada"""
        cls.test_user_id = "test_user_standalone"
        cls.base_url = BASE_URL
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        
        # Inicia o servidor em background
        cls.server_thread = threading.Thread(
            target=cls._run_server,
            daemon=True
        )
        cls.server_thread.start()
        
        # Aguarda o servidor estar pronto
        cls._wait_for_server()
    
    @classmethod
    def _run_server(cls):
        """Executa o servidor Flask"""
        cls.app.run(host='127.0.0.1', port=5001, debug=False, use_reloader=False)
    
    @classmethod
    def _wait_for_server(cls, max_attempts=30):
        """Aguarda o servidor estar pronto"""
        for attempt in range(max_attempts):
            try:
                response = requests.get(f"{cls.base_url}/health", timeout=1)
                if response.status_code == 200:
                    print(f"✅ Servidor pronto após {attempt + 1} tentativas")
                    return
            except Exception:
                pass
            time.sleep(0.5)
        
        raise Exception("❌ Servidor não ficou pronto a tempo")
    
    def test_01_health_check(self):
        """Testa se o servidor está funcionando"""
        response = requests.get(f"{self.base_url}/health", timeout=5)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        print("✅ Health check OK")
    
    def test_02_fluxo_conversa_completo(self):
        """Testa o fluxo completo de uma conversa"""
        mensagens_e_respostas = [
            ("Olá", "Qual é o seu nome"),
            ("João Standalone", "Muito bem, João Standalone"),
            ("15/07/2025", "Perfeito! Data: 15/07/2025"),
            ("manhã", "Consulta marcada com sucesso")
        ]
        
        for mensagem, resposta_esperada in mensagens_e_respostas:
            with self.subTest(mensagem=mensagem):
                response = requests.post(
                    f"{self.base_url}/mensagem",
                    json={"user_id": self.test_user_id, "mensagem": mensagem}
                )
                
                self.assertEqual(response.status_code, 200)
                data = response.json()
                self.assertIn(resposta_esperada, data['resposta'])
                print(f"✅ Mensagem '{mensagem}' processada corretamente")
    
    def test_03_consultas_salvas(self):
        """Testa se as consultas foram salvas no banco"""
        response = requests.get(f"{self.base_url}/consultas")
        self.assertEqual(response.status_code, 200)
        
        consultas = response.json()
        self.assertGreater(len(consultas), 0, "Nenhuma consulta encontrada")
        
        # Verifica se nossa consulta de teste está lá
        consulta_teste = next(
            (c for c in consultas if c['user_id'] == self.test_user_id),
            None
        )
        self.assertIsNotNone(consulta_teste, "Consulta de teste não encontrada")
        print(f"✅ {len(consultas)} consulta(s) encontrada(s) no banco")
    
    def test_04_historico_conversa(self):
        """Testa se o histórico da conversa foi salvo"""
        response = requests.get(f"{self.base_url}/historico/{self.test_user_id}")
        self.assertEqual(response.status_code, 200)
        
        historico = response.json()
        self.assertGreater(len(historico), 0, "Nenhum histórico encontrado")
        print(f"✅ Histórico com {len(historico)} interações salvo")
    
    def test_05_estatisticas(self):
        """Testa o endpoint de estatísticas"""
        response = requests.get(f"{self.base_url}/estatisticas")
        self.assertEqual(response.status_code, 200)
        
        stats = response.json()
        required_fields = ['total_consultas', 'usuarios_unicos', 'consultas_por_periodo']
        
        for field in required_fields:
            self.assertIn(field, stats, f"Campo {field} não encontrado nas estatísticas")
        
        self.assertGreaterEqual(stats['total_consultas'], 1)
        print(f"✅ Estatísticas: {stats['total_consultas']} consultas, {stats['usuarios_unicos']} usuários")
    
    def test_06_reiniciar_conversa(self):
        """Testa a funcionalidade de reiniciar conversa"""
        response = requests.post(f"{self.base_url}/conversa/reiniciar/{self.test_user_id}")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('sucesso', data['mensagem'])
        print("✅ Conversa reiniciada com sucesso")
    
    def test_07_status_conversa(self):
        """Testa o endpoint de status da conversa"""
        response = requests.get(f"{self.base_url}/conversa/status/{self.test_user_id}")
        self.assertEqual(response.status_code, 200)
        
        status = response.json()
        self.assertIn('estado', status)
        self.assertIn('user_id', status)
        print(f"✅ Status da conversa obtido: {status['estado']}")

if __name__ == "__main__":
    unittest.main(verbosity=2)
