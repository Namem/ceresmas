import os
from src.agents.manager import ManagerAgent
from src.database.models import init_db

init_db()

def main():
    print("\n🌱 --- SISTEMA CERES MAS (V4.1) ---")
    print("Dica: Digite 'sair' para encerrar.\n")
    
    manager = ManagerAgent()
    historico_chat = "" # <--- AQUI NASCE A MEMÓRIA
    
    while True:
        user_input = input("produtor@sorriso:~$ ")
        if user_input.lower() in ['sair', 'exit']:
            break
            
        try:
            # Passamos o histórico junto com a nova mensagem
            resultado = manager.processar_entrada(user_input, historico_chat)
            
            print(f"\n🤖 CERES:\n{resultado}\n")
            print("-" * 50)
            
            # Atualizamos a memória com o que acabou de acontecer (limitando o tamanho para não estourar os tokens)
            historico_chat += f"Produtor: {user_input}\nCeres: {resultado}\n"
            
            # Mantém apenas as últimas 2 interações (4 linhas) no buffer para focar no contexto imediato
            linhas_historico = historico_chat.strip().split('\n')
            if len(linhas_historico) > 4:
                historico_chat = '\n'.join(linhas_historico[-4:]) + '\n'
                
        except Exception as e:
            print(f"❌ Erro Crítico: {e}")

if __name__ == "__main__":
    main()