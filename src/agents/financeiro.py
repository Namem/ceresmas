import os
from crewai import Agent, Task, Crew, Process, LLM
from src.tools.financeiro import FerramentasFinanceiras

class FinanceiroAgent:
    def executar(self, texto_produtor: str):
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
                    goal='Gerenciar os custos agrícolas, registrando novas despesas e calculando relatórios de Custo Operacional Efetivo (COE).',
                    backstory='Você é um contador especializado em agronegócio. Você é metódico. Se o produtor mandar um gasto, você registra. Se ele pedir um balanço, você calcula o COE.',
                    verbose=True,
                    memory=False, 
                    llm=llm_engine,
                    # ATENÇÃO AQUI: Adicionamos a nova tool na lista!
                    tools=[FerramentasFinanceiras.registrar_custo, FerramentasFinanceiras.calcular_coe]
                )

                tarefa = Task(
                    description=f"""
                    O produtor enviou a seguinte mensagem: "{texto_produtor}"
                    
                    REGRA DE SISTEMA ABSOLUTA: Você NÃO PODE responder com suposições ou pedir dados se a intenção for uma consulta. Você DEVE acionar uma ferramenta.
                    
                    - Se a mensagem relatar um NOVO GASTO (ex: "comprei", "paguei"): Use a ferramenta 'registrar_custo'.
                    - Se a mensagem pedir um RESUMO, TOTAL ou RELATÓRIO (ex: "quanto gastei", "puxa o total"): Use OBRIGATORIAMENTE a ferramenta 'consultar_relatorio_coe' passando o argumento filtro="todos".
                    
                    Após receber os dados reais do banco de dados através da ferramenta, formate-os e apresente ao produtor.
                    """,
                    expected_output="Relatório numérico gerado pela ferramenta ou confirmação de registro.",
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

        return "Opa, meus sistemas contábeis estão fora do ar. Tenta de novo daqui a pouco!"