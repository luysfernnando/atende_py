# tests/run_all_tests.py
"""
Executador de todos os testes do projeto
Combina testes unitários e de integração
"""

import unittest
import sys
import os

# Adiciona o diretório raiz ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_unit_tests():
    """Executa testes unitários"""
    print("🧪 EXECUTANDO TESTES UNITÁRIOS")
    print("=" * 40)
    
    # Carrega testes unitários
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Adiciona testes de modelos
    from tests.test_models import TestConsulta, TestConversa
    suite.addTests(loader.loadTestsFromTestCase(TestConsulta))
    suite.addTests(loader.loadTestsFromTestCase(TestConversa))
    
    # Executa testes unitários
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

def run_integration_tests():
    """Executa testes de integração"""
    print("\n🔗 EXECUTANDO TESTES DE INTEGRAÇÃO")
    print("=" * 40)
    print("⚠️  Certifique-se de que o servidor está rodando: python app.py")
    print()
    
    # Executa o teste de integração
    from tests.test_chatbot_integration import run_manual_test
    return run_manual_test()

def main():
    """Executa todos os testes"""
    print("🚀 EXECUTANDO SUITE COMPLETA DE TESTES")
    print("=" * 50)
    print("📁 Estrutura de testes organizada:")
    print("   - tests/test_models.py (testes unitários)")
    print("   - tests/test_chatbot_integration.py (testes de integração)")
    print()
    
    # Executa testes unitários
    unit_success = run_unit_tests()
    
    # Executa testes de integração
    integration_success = run_integration_tests()
    
    # Resultado final
    print("\n📊 RESULTADO FINAL")
    print("=" * 30)
    
    if unit_success and integration_success:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Arquitetura SOLID + KISS validada!")
        print("✅ Funcionalidades do chatbot funcionando!")
        return True
    else:
        print("⚠️  Alguns testes falharam:")
        if not unit_success:
            print("   ❌ Testes unitários falharam")
        if not integration_success:
            print("   ❌ Testes de integração falharam")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)