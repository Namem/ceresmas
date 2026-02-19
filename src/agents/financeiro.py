import os
from crewai import Agent, Task, Crew, Process, LLM
from src.tools.financeiro import FerramentasFinanceiras # Assumindo que essa tool existe
from dotenv import load_dotenv

load_dotenv()

class FinanceiroAgent:
    def executar(self, texto_produtor: str):
        my_llm = LLM(model="gemini/gemini-2.5-flash", api_key=os.getenv("GOOGLE_API_KEY"))

        agente = Agent(
            role='Gerente Financeiro Ceres',
            goal='Registrar custos agrícolas com precisão contábil (ACID).',
            backstory='Contador especializado que converte linguagem natural em SQL.',
            verbose=True,
            llm=my_llm,
            tools=[FerramentasFinanceiras.registrar_custo]
        )

        task = Task(
            description=f"""
            Input: "{texto_produtor}"
            1. Extraia: Item, Valor, Quantidade, Unidade, Categoria.
            2. Use a tool 'Registrar Custo' para persistir no PostgreSQL.
            """,
            expected_output="Confirmação de registro contábil.",
            agent=agente
        )

        crew = Crew(agents=[agente], tasks=[task], process=Process.sequential)
        return crew.kickoff()