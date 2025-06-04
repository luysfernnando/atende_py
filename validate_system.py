#!/usr/bin/env python3
"""
Script de validação para verificar se o sistema está funcionando corretamente
Usado para verificar a configuração antes de fazer push
"""

import sys
import os
import subprocess

def run_command(cmd, description):
    """Executa um comando e retorna o resultado"""
    print(f"🔍 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=os.getcwd())
        if result.returncode == 0:
            print(f"✅ {description} - OK")
            return True
        else:
            print(f"❌ {description} - FALHOU")
            print(f"Erro: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - ERRO: {e}")
        return False

def check_python_imports():
    """Verifica se as importações Python estão funcionando"""
    print("🔍 Verificando importações Python...")
    try:
        # Testa importações principais
        from src.models.consulta import Consulta
        from src.models.conversa import Conversa
        from src.services.chatbot_service import ChatbotService
        print("✅ Importações Python - OK")
        return True
    except Exception as e:
        print(f"❌ Importações Python - FALHOU: {e}")
        return False

def main():
    """Executa todas as verificações"""
    print("🚀 VALIDAÇÃO DO SISTEMA ATENDE-PY")
    print("=" * 50)
    
    checks = []
    
    # Verifica se está no diretório correto
    if not os.path.exists('app.py'):
        print("❌ Não está no diretório do projeto!")
        sys.exit(1)
    
    # Verifica importações Python
    checks.append(check_python_imports())
    
    # Verifica arquivos importantes
    required_files = [
        'app.py',
        'src/models/consulta.py',
        'src/models/conversa.py',
        'src/services/chatbot_service.py',
        'tests/test_models.py'
    ]
    
    print("🔍 Verificando arquivos necessários...")
    files_ok = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - NÃO ENCONTRADO")
            files_ok = False
    
    checks.append(files_ok)
    
    # Tenta executar teste básico
    print("🔍 Executando teste básico...")
    try:
        from src.models.consulta import Consulta
        consulta = Consulta("Teste", "15/06/2025", "manhã", "test_user")
        if consulta.nome == "Teste":
            print("✅ Teste básico - OK")
            checks.append(True)
        else:
            print("❌ Teste básico - FALHOU")
            checks.append(False)
    except Exception as e:
        print(f"❌ Teste básico - ERRO: {e}")
        checks.append(False)
    
    # Resultado final
    print("\n" + "=" * 50)
    if all(checks):
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Sistema pronto para GitHub Actions")
        return 0
    else:
        print("⚠️ ALGUNS TESTES FALHARAM")
        print("❌ Corrija os problemas antes de fazer push")
        return 1

if __name__ == "__main__":
    sys.exit(main())
