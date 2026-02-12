import os
from crewai import Agent, Task, Crew, Process, LLM
from src.tools.rag_tool import RagTools

class AgronomoAgent:
    """
    Classe responsável por instanciar o Agente Agrônomo e suas tarefas.
    """

    def criar_agente(self):
        # CONFIGURAÇÃO DO CÉREBRO (LLM)
        # Usamos a classe nativa LLM do CrewAI para evitar erros de compatibilidade.
        # O modelo "gemini/gemini-1.5-flash" é o mais estável e rápido para RAG.
        llm_engine = LLM(
            model="gemini/gemini-2.5-flash",
            api_key=os.getenv("GOOGLE_API_KEY")
        )

        return Agent(
            role='Engenheiro Agrônomo Sênior (Especialista em Hortaliças)',
            goal='Fornecer diagnósticos precisos e planos de manejo baseados EXCLUSIVAMENTE em manuais da Embrapa.',
            backstory="""
                Você é o Engenheiro Agronomo Watson, um especialista com 20 anos de experiência 
                em Olericultura (Hortaliças) no clima tropical de Sorriso-MT.
                
                Sua missão é ajudar pequenos produtores rurais a resolverem problemas de pragas, 
                doenças e manejo nutricional.
                
                SUAS REGRAS DE OURO (SISTEMA DE SEGURANÇA):
                1. Você NÃO "acha" nada. Você consulta a base de conhecimento.
                2. Ao responder, você DEVE citar a fonte técnica (Ex: "Segundo o Manual da Embrapa...").
                3. Se a informação não estiver na base, diga: "Não encontrei dados oficiais sobre isso nos manuais carregados".
                4. Seja didático, mas tecnicamente rigoroso. O produtor precisa entender, mas a solução deve ser científica.
            """,
            verbose=True,
            allow_delegation=False,
            tools=[RagTools().search_knowledge_base], # Ferramenta de RAG Local
            llm=llm_engine
        )

    def responder_duvida(self, pergunta: str):
        """
        Cria a tarefa (Task) e executa o processo de raciocínio.
        """
        agente = self.criar_agente()

        task_diagnostico = Task(
            description=f"""
                Analise a seguinte dúvida do produtor rural de Sorriso-MT:
                "{pergunta}"
                
                PASSOS PARA EXECUÇÃO:
                1. Use a ferramenta 'Consultar Manuais Embrapa' para buscar o contexto técnico sobre a dúvida.
                2. Analise as informações recuperadas dos PDFs.
                3. Formule uma resposta técnica, citando o manejo correto.
                4. Se houver recomendação química ou biológica, cite as dosagens se disponíveis no texto.
            """,
            expected_output="Um parecer técnico formatado, citando as fontes da Embrapa e sugerindo ações práticas.",
            agent=agente
        )

        crew = Crew(
            agents=[agente],
            tasks=[task_diagnostico],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        return result