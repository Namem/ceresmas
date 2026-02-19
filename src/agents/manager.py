import os
from crewai import Agent, Task, Crew, Process, LLM
from src.agents.agronomo import AgronomoAgent
from src.agents.financeiro import FinanceiroAgent # Terá de refatorar o financeiro.py (ver abaixo)

class ManagerAgent:
    def __init__(self):
        self.llm = LLM(
            model="gemini/gemini-2.5-flash",
            api_key=os.getenv("GOOGLE_API_KEY")
        )

    def processar_entrada(self, entrada_usuario: str):
        """
        Função principal que o main.py chamará.
        """
        # 1. Agente de Triagem (Rápido e Barato)
        triagem_agent = Agent(
            role='Gerente de Triagem Ceres',
            goal='Classificar a demanda do produtor em FINANCEIRO, AGRONOMICO ou GERAL.',
            backstory='Você é o recepcionista inteligente do sistema. Você não resolve problemas, apenas direciona.',
            verbose=True,
            llm=self.llm,
            allow_delegation=False
        )

        task_triagem = Task(
            description=f"""
            Analise a mensagem do produtor: "{entrada_usuario}"
            
            Responda APENAS com uma das palavras:
            - FINANCEIRO (se falar de custos, compras, diesel, valores, dinheiro)
            - AGRONOMICO (se falar de pragas, doenças, plantio, adubo, bichos)
            - GERAL (se for 'olá', 'tudo bem' ou fora do contexto)
            """,
            expected_output="Uma única palavra classificatória.",
            agent=triagem_agent
        )

        crew_triagem = Crew(agents=[triagem_agent], tasks=[task_triagem])
        classificacao = crew_triagem.kickoff().raw.strip().upper()
        
        print(f"\n🚦 [MANAGER] Classificação: {classificacao}")

        # 2. Roteamento (Routing Pattern)
        if "FINANCEIRO" in classificacao:
            return FinanceiroAgent().executar(entrada_usuario)
        
        elif "AGRONOMICO" in classificacao:
            return AgronomoAgent().executar(entrada_usuario)
            
        else:
            return "Olá! Sou o Ceres MAS. Posso ajudar com custos da fazenda ou dúvidas técnicas da lavoura."