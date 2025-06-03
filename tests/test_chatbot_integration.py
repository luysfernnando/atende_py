# tests/test_chatbot_integration.py
"""
Testes de integração para o chatbot com nova arquitetura
Testa o funcionamento completo do sistema end-to-end
"""

import requests
import json
import unittest
from typing import Dict, Any

BASE_URL = "http://localhost:5000"

class TestChatbotIntegration(unittest.TestCase):
    """Testes de integração para o chatbot"""
    
    @classmethod
    def setUpClass(cls):
        """Configuração inicial dos testes"""
        cls.test_user_id = "test_user_integration"
        cls.base_url = BASE_URL
    
    def test_01_health_check(self):
        """Testa se o servidor está funcionando"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data['status'], 'ok')
            print("✅ Health check OK")
        except requests.exceptions.ConnectionError:
            self.fail("❌ Servidor não está rodando. Execute: python app.py")
    
    def test_02_fluxo_conversa_completo(self):
        """Testa o fluxo completo de uma conversa"""
        mensagens_e_respostas = [
            ("Olá", "Qual é o seu nome"),
            ("João Teste", "Muito bem, João Teste"),
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

def run_manual_test():
    """Executa testes manuais quando chamado diretamente"""
    print("🏗️  TESTES DA ARQUITETURA REFATORADA")
    print("=" * 50)
    print("📋 Executando testes de integração...")
    print()
    
    # Verifica se o servidor está rodando
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        if response.status_code != 200:
            print("❌ Servidor não está respondendo corretamente")
            return False
    except:
        print("❌ Erro: Servidor não está rodando")
        print("   Execute: python app.py")
        return False
    
    # Executa os testes
    suite = unittest.TestLoader().loadTestsFromTestCase(TestChatbotIntegration)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print(f"\n📊 RESULTADO DOS TESTES:")
    print(f"✅ Sucessos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Falhas: {len(result.failures)}")
    print(f"🔥 Erros: {len(result.errors)}")
    
    if result.wasSuccessful():
        print(f"\n🎉 TODOS OS TESTES PASSARAM!")
        print("🏗️  Arquitetura SOLID + KISS validada!")
        return True
    else:
        print(f"\n⚠️  Alguns testes falharam")
        return False

if __name__ == "__main__":
    run_manual_test()