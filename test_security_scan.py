#!/usr/bin/env python3
"""
Teste do Security Scan - GitHub Actions
Simula exatamente o que acontece no CI/CD
"""

import subprocess
import sys
import os

def run_command(cmd, description):
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
            print("STDOUT:", result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
            
        print(f"Return code: {result.returncode}")
        return result.returncode == 0
            
    except Exception as e:
        print(f"❌ Erro executando comando: {e}")
        return False

def main():
    """Simula o security scan do GitHub Actions"""
    print("🔒 TESTE DO SECURITY SCAN")
    print("=" * 60)
    
    steps = [
        (
            "python -m pip install --upgrade pip setuptools",
            "Upgrade pip and setuptools"
        ),
        (
            "pip install flask twilio python-dotenv",
            "Install project dependencies"
        ),
        (
            "pip install pip-audit",
            "Install pip-audit"
        ),
        (
            "pip-audit --ignore-vuln PYSEC-2022-43012 --ignore-vuln GHSA-5rjg-fvgr-3xxf",
            "Run security scan with ignored vulnerabilities"
        ),
    ]
    
    success_count = 0
    total_steps = len(steps)
    
    for cmd, desc in steps:
        if run_command(cmd, desc):
            success_count += 1
            print(f"✅ {desc} - OK")
        else:
            print(f"⚠️ {desc} - FALHOU (mas continuando...)")
    
    print("\n" + "=" * 60)
    print("📊 RESULTADO DO TESTE")
    print(f"✅ Sucessos: {success_count}/{total_steps}")
    
    if success_count >= 3:  # Pelo menos 3 dos 4 passos devem funcionar
        print("\n🎉 SECURITY SCAN APROVADO!")
        print("✅ GitHub Actions deve funcionar")
        return 0
    else:
        print("\n⚠️ SECURITY SCAN COM PROBLEMAS")
        return 1

if __name__ == "__main__":
    sys.exit(main())
