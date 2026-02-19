import os 
from src.agents.manager import ManagerAgent
from src.database.models import init_db

init_db

def main():
    print("\n🌱 --- SISTEMA CERES MAS (V4.0) ---")
    print("Dica: Digite 'sair' para encerrar.\n")
    
    manager = ManagerAgent()

    while True:
        user_input = input ("produtor@:~$")
        if user_input.lower() in ['sair', 'exit']:
            break

        try:
            resultado = manager.processar_entrada(user_input)
            print(f"\n🤖 CERES:\n{resultado}\n")
            print("-" * 50)
        except Exception as e:
            print(f"❌ ERRO: {e}")
            print("-" * 50)

if __name__ == "__main__":
    main()