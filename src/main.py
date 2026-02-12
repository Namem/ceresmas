import os
import sys
from dotenv import load_dotenv

# Adiciona o diretório raiz ao path do Python para evitar erros de importação
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.agronomo import AgronomoAgent

def main():
    # 1. Carrega Variáveis de Ambiente
    load_dotenv()
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ ERRO: GOOGLE_API_KEY não encontrada no arquivo .env")
        return

    print("##########################################################")
    print("🚀 CERES MAS - SISTEMA DE ASSISTÊNCIA AO PRODUTOR RURAL")
    print("   Modo: Console (Sprint 1)")
    print("##########################################################")

    # 2. Loop de Interação
    agente = AgronomoAgent()
    
    while True:
        pergunta = input("\n👨‍🌾 DIGITE SUA DÚVIDA (ou 'sair'): ")
        
        if pergunta.lower() in ['sair', 'exit', 'q']:
            print("👋 Encerrando o sistema Ceres.")
            break

        print("\n🤖 O Engenheiro Watson está consultando a biblioteca da Embrapa...")
        print("   (Isso pode levar alguns segundos enquanto lemos o ChromaDB e consultamos o LLM)\n")
        
        try:
            # 3. Execução do Agente
            resposta = agente.responder_duvida(pergunta)
            
            print("\n================ RESPOSTA DO AGRÔNOMO ================")
            print(resposta)
            print("======================================================\n")
            
        except Exception as e:
            print(f"❌ Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()