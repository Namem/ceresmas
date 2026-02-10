import os
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
from tools_financeiro import FerramentasFinanceiras

load_dotenv()

# Configura o Cérebro (Gemini 2.0)
my_llm = LLM(
    model="gemini-2.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY")
)

# 1. Persona do Agente
agente_financas = Agent(
    role='Gerente Financeiro Ceres',
    goal='Registrar custos agrícolas com precisão contábil.',
    backstory='Você é um contador especializado em agronegócio. Você recebe mensagens informais de produtores no WhatsApp e lança no sistema ERP.',
    verbose=True,
    memory=False,
    llm=my_llm,
    tools=[FerramentasFinanceiras.registrar_custo] # Damos a ferramenta para ele
)

# 2. O Teste (Simulação de um Produtor falando)
texto_produtor = "Ô Ceres, hoje eu peguei 500 litros de diesel pro trator lá no posto, deu 3500 reais tudo."

tarefa = Task(
    description=f"""
    O produtor enviou a seguinte mensagem: "{texto_produtor}"
    
    1. Interprete o texto e extraia: Item, Valor, Quantidade, Unidade e Categoria.
    2. USE A TOOL 'Registrar Custo de Produção' para salvar no banco de dados.
    3. Responda confirmando o registro.
    """,
    expected_output="Confirmação de registro.",
    agent=agente_financas
)

# 3. Execução
crew = Crew(
    agents=[agente_financas],
    tasks=[tarefa],
    process=Process.sequential
)

print("--- 🚜 RODANDO AGENTE FINANCEIRO (CERES MAS) ---")
resultado = crew.kickoff()
print("\n################ RESULTADO ################\n")
print(resultado)