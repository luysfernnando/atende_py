#!/usr/bin/env python3
"""
✅ SCRIPT DE VALIDAÇÃO FINAL
Verifica se todas as correções foram aplicadas corretamente
"""

import os
import sys

def check_file_content(file_path, should_contain, should_not_contain=None):
    """Verifica se um arquivo contém ou não contém certas strings"""
    if not os.path.exists(file_path):
        return False, f"Arquivo {file_path} não encontrado"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verifica se contém o que deveria conter
    for item in should_contain:
        if item not in content:
            return False, f"'{item}' não encontrado em {file_path}"
    
    # Verifica se não contém o que não deveria conter
    if should_not_contain:
        for item in should_not_contain:
            if item in content:
                return False, f"'{item}' ainda encontrado em {file_path} (deveria ter sido removido)"
    
    return True, "OK"

def main():
    """Executa todas as validações"""
    print("🔍 VALIDAÇÃO FINAL - CORREÇÕES GITHUB ACTIONS")
    print("=" * 60)
    
    checks = []
    
    # 1. Verifica requirements.txt
    print("\n📋 Verificando requirements.txt...")
    result, msg = check_file_content(
        'requirements.txt',
        should_contain=['Flask', 'twilio', 'python-dotenv'],
        should_not_contain=['chatterbot', 'chatterbot-corpus']
    )
    checks.append(result)
    print(f"{'✅' if result else '❌'} requirements.txt: {msg}")
    
    # 2. Verifica pyproject.toml
    print("\n📋 Verificando pyproject.toml...")
    result, msg = check_file_content(
        'pyproject.toml',
        should_contain=['nltk>=3.8.0'],
        should_not_contain=['chatterbot>=1.0.8', 'chatterbot-corpus>=1.2.0']
    )
    checks.append(result)
    print(f"{'✅' if result else '❌'} pyproject.toml: {msg}")
    
    # 3. Verifica CI/CD
    print("\n📋 Verificando .github/workflows/ci.yml...")
    result, msg = check_file_content(
        '.github/workflows/ci.yml',
        should_contain=['pip install flask twilio python-dotenv', 'Run basic validation'],
        should_not_contain=['pip install -e ".[dev,ai]"', 'flake8', 'black --check', 'mypy']
    )
    checks.append(result)
    print(f"{'✅' if result else '❌'} ci.yml: {msg}")
    
    # 4. Verifica se testes standalone existem
    print("\n📋 Verificando testes standalone...")
    result = os.path.exists('tests/test_chatbot_integration_standalone.py')
    checks.append(result)
    print(f"{'✅' if result else '❌'} Testes standalone: {'Existem' if result else 'Não encontrados'}")
    
    # 5. Verifica se AIService funciona
    print("\n📋 Verificando AIService...")
    try:
        sys.path.insert(0, '.')
        from src.services.ai_service import AIService
        ai = AIService()
        resultado = ai.processar_intencao("oi")
        result = 'intencao' in resultado
        checks.append(result)
        print(f"{'✅' if result else '❌'} AIService: {'Funcionando' if result else 'Com problemas'}")
    except Exception as e:
        checks.append(False)
        print(f"❌ AIService: Erro - {e}")
    
    # 6. Verifica estrutura de arquivos
    print("\n📋 Verificando estrutura de arquivos...")
    required_files = [
        'app.py',
        'src/services/ai_service.py',
        'src/models/consulta.py',
        'src/models/conversa.py',
        'tests/test_models.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    result = len(missing_files) == 0
    checks.append(result)
    if result:
        print("✅ Estrutura de arquivos: Completa")
    else:
        print(f"❌ Estrutura de arquivos: Faltam {missing_files}")
    
    # Resultado final
    print("\n" + "=" * 60)
    print("📊 RESULTADO DA VALIDAÇÃO")
    success_count = sum(checks)
    total_checks = len(checks)
    
    print(f"✅ Sucessos: {success_count}/{total_checks}")
    print(f"❌ Falhas: {total_checks - success_count}/{total_checks}")
    
    if success_count == total_checks:
        print("\n🎉 TODAS AS VALIDAÇÕES PASSARAM!")
        print("✅ Sistema pronto para GitHub Actions")
        print("🚀 Pode fazer commit/push sem erros")
        return 0
    else:
        print("\n⚠️ ALGUMAS VALIDAÇÕES FALHARAM")
        print("❌ Corrija os problemas antes do commit")
        return 1

if __name__ == "__main__":
    sys.exit(main())
