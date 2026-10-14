"""Executa toda a suíte de testes do projeto."""
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def main():
    test_files = [
        PROJECT_ROOT / "tests" / "test_customizer.py",
        PROJECT_ROOT / "tests" / "test_renderer.py",
    ]

    for test_file in test_files:
        print(f"\n=== Executando {test_file.name} ===")
        result = subprocess.run([sys.executable, str(test_file)], cwd=str(PROJECT_ROOT))
        if result.returncode != 0:
            print(f"[FALHA] Teste falhou: {test_file.name}")
            sys.exit(result.returncode)

    print("\n==========================================")
    print("[SUCESSO] Todos os testes passaram 100%!")
    print("==========================================\n")


if __name__ == "__main__":
    main()
