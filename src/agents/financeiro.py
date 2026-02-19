import os
from crewai import Agent, Task, Crew, Process, LLM
from src.tools.financeiro import FerramentasFinanceiras

class FinanceiroAgent:
    def executar(self, texto_produtor: str):
        # LISTA DE FALLBACK (Baseada no painel real do Google AI Studio)
        modelos_fallback = [
            "gemini/gemini-2.5-flash-lite",
            "gemini/gemini-3-flash",
            "gemini/gemini-2.5-flash"
        ]

        for modelo_atual in modelos_fallback:
            try:
                llm_engine = LLM(
                    model=modelo_atual,
                    api_key=os.getenv("GOOGLE_API_KEY")
                )

                agente_financas = Agent(
                    role='Gerente Financeiro Ceres',
                    goal='Registrar custos agrícolas com precisão contábil.',
                    backstory='Você é um contador especializado em agronegócio. Você recebe mensagens informais de produtores no WhatsApp e lança no sistema ERP.',
                    verbose=True,
                    memory=False, # Financeiro avalia cada custo de forma isolada
                    llm=llm_engine,
                    tools=[FerramentasFinanceiras.registrar_custo]
                )

                tarefa = Task(
                    description=f"""
                    O produtor enviou a seguinte mensagem: "{texto_produtor}"
                    
                    1. Interprete o texto e extraia: Item, Valor, Quantidade, Unidade e Categoria.
                    2. USE A TOOL 'Registrar Custo' para persistir no PostgreSQL.
                    3. Responda confirmando o registro de forma amigável.
                    """,
                    expected_output="Confirmação de registro contábil.",
                    agent=agente_financas
                )

                crew = Crew(
                    agents=[agente_financas],
                    tasks=[tarefa],
                    process=Process.sequential
                )

                return crew.kickoff().raw

            except Exception as e:
                print(f"⚠️ [FALLBACK FINANCEIRO] Falha no modelo {modelo_atual}. Tentando o próximo... Erro: {str(e)[:50]}")
                continue

        return "Opa, não consegui registrar essa despesa agora devido a uma falha na conexão com o banco de dados. Tenta de novo daqui a pouco!"