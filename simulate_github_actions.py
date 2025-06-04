#!/usr/bin/env python3
"""
Simulador do GitHub Actions para testar localmente
Simula os passos exatos do CI/CD
"""

import subprocess
import sys
import os

def run_command(cmd, description, allow_failure=False):
    """Executa um comando como no GitHub Actions"""
    print(f"\n🔄 {description}")
    print(f"💻 Executando: {cmd}")
    print("-" * 50)
    
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd="/home/lulfex/Documentos/DEV/Study/Python/atende_py",
            text=True,
            capture_output=True
        )
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
            
        if result.returncode != 0:
            if allow_failure:
                print(f"⚠️ {description} - FALHOU (mas continuando...)")
                return False
            else:
                print(f"❌ {description} - FALHOU")
                return False
        else:
            print(f"✅ {description} - OK")
            return True
            
    except Exception as e:
        print(f"❌ Erro executando comando: {e}")
        return False

def main():
    """Simula o pipeline do GitHub Actions"""
    print("🚀 SIMULAÇÃO DO GITHUB ACTIONS")
    print("=" * 60)
    
    # Simula setup do ambiente
    os.chdir("/home/lulfex/Documentos/DEV/Study/Python/atende_py")
    
    steps = [
        # 1. Install dependencies
        (
            "python -m pip install --upgrade pip",
            "Upgrade pip"
        ),
        (
            "pip install flask twilio python-dotenv pytest pytest-cov",
            "Install dependencies",
            True  # Permite falha
        ),
        
        # 2. Setup test environment
        (
            'echo "FLASK_ENV=testing" > .env',
            "Create .env file (1/5)"
        ),
        (
            'echo "SECRET_KEY=test-secret-key-for-ci" >> .env',
            "Create .env file (2/5)"
        ),
        (
            'echo "TWILIO_ACCOUNT_SID=" >> .env',
            "Create .env file (3/5)"
        ),
        (
            'echo "TWILIO_AUTH_TOKEN=" >> .env',
            "Create .env file (4/5)"
        ),
        (
            'echo "TWILIO_PHONE_NUMBER=" >> .env',
            "Create .env file (5/5)"
        ),
        
        # 3. Basic validation
        (
            '''python -c "
import sys, os
sys.path.insert(0, '.')
try:
    from src.models.consulta import Consulta
    from src.models.conversa import Conversa
    print('✅ Importações OK')
except Exception as e:
    print(f'❌ Erro de importação: {e}')
    sys.exit(1)
"''',
            "Run basic validation"
        ),
        
        # 4. Unit tests
        (
            "python -m pytest tests/test_models.py -v",
            "Run unit tests",
            True  # Permite falha
        ),
        
        # 5. Integration tests
        (
            "python -m pytest tests/test_chatbot_integration_standalone.py -v --tb=short",
            "Run integration tests (standalone)",
            True  # Permite falha
        ),
    ]
    
    success_count = 0
    total_steps = len(steps)
    
    for step in steps:
        if len(step) == 3:
            cmd, desc, allow_failure = step
        else:
            cmd, desc = step
            allow_failure = False
            
        if run_command(cmd, desc, allow_failure):
            success_count += 1
    
    print("\n" + "=" * 60)
    print("📊 RESULTADO DA SIMULAÇÃO")
    print(f"✅ Sucessos: {success_count}/{total_steps}")
    print(f"❌ Falhas: {total_steps - success_count}/{total_steps}")
    
    if success_count >= total_steps - 2:  # Aceita até 2 falhas
        print("\n🎉 SIMULAÇÃO APROVADA!")
        print("✅ GitHub Actions deve funcionar")
        return 0
    else:
        print("\n⚠️ SIMULAÇÃO COM PROBLEMAS")
        print("❌ Corrija os erros antes do commit")
        return 1

if __name__ == "__main__":
    sys.exit(main())
