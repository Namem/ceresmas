import os
import sys
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv

# 1. Carregar variáveis
load_dotenv()
chave_google = os.getenv("GOOGLE_API_KEY")

if not chave_google:
    print("❌ ERRO: Sem chave no .env")
    sys.exit(1)

print(f"--- 🚀 INICIANDO COM GEMINI 2.0 FLASH (Chave: {chave_google[:5]}...) ---")

# 2. Configuração do LLM (Usando o modelo CONFIRMADO na sua lista)
try:
    # O prefixo 'gemini/' diz pro CrewAI usar o conector do Google
    # O sufixo 'gemini-2.0-flash' é o modelo que vimos na sua lista
    my_llm = LLM(
        model="gemini/gemini-2.0-flash",
        api_key=chave_google
    )
except Exception as e:
    print(f"❌ Erro na configuração do LLM: {e}")
    sys.exit(1)

# 3. Criar o Agente
agente_teste = Agent(
    role='Agente de Teste Sênior',
    goal='Validar o ambiente',
    backstory='Você é um agente rodando no estado da arte da IA.',
    verbose=True,
    memory=False, 
    llm=my_llm
)

# 4. Criar a Tarefa
tarefa = Task(
    description='Responda: "Ambiente AgroLink Operacional com Gemini 2.0!"',
    expected_output='Frase de sucesso.',
    agent=agente_teste
)

# 5. Executar
crew = Crew(
    agents=[agente_teste],
    tasks=[tarefa],
    process=Process.sequential
)

try:
    print("--- ⚡ ENVIANDO PARA O GEMINI 2.0... ---")
    resultado = crew.kickoff()
    print("\n\n################ SUCESSO ################")
    print(resultado)
except Exception as e:
    print(f"\n❌ ERRO: {e}")