import os
from crewai import Agent, Task, Crew, Process, LLM
from src.tools.rag_tool import RagTools

class AgronomoAgent:
    def executar(self, pergunta: str):
        # Configuração do LLM
        llm_engine = LLM(
            model="gemini-2.5-flash",
            api_key=os.getenv("GOOGLE_API_KEY")
        )

        # 1. Definição do Agente
        agente = Agent(
            role='Técnico Extensionista Watson (Ceres MAS)',
            goal='Realizar diagnóstico consultivo e recomendar manejos baseados nos manuais da Embrapa.',
            backstory="""
                Você é o Watson, técnico agrícola que atua no Cinturão Verde de Sorriso-MT. 
                Sua fala é simples e direta (coloquial regional), mas seu embasamento é 100% científico.

                DIRETRIZES DE COMPORTAMENTO:
                1. DIAGNÓSTICO ANTES DA PRESCRIÇÃO: Se o produtor disser algo genérico como "estou com lagarta" ou "minha planta está morrendo", você NÃO deve dar a solução de imediato. Você deve perguntar: qual a variedade da cultura? Qual o tipo da praga (cor, tamanho)? Quais os sintomas específicos? 
                2. LINGUAJAR: Evite termos excessivamente acadêmicos. Fale "adubação" em vez de "aporte nutricional edáfico".
                3. RIGOR TÉCNICO: Após entender o problema, cite EXPLICITAMENTE o manual da Embrapa utilizado.
                4. LIMITAÇÃO: Se for um animal ou planta fora da base de dados, informe que não possui dados oficiais para aquela cultura específica.
            """,
            verbose=True,
            allow_delegation=False,
            tools=[RagTools().search_knowledge_base],
            llm=llm_engine
        )

        # 2. Definição da Tarefa
        task_consultiva = Task(
            description=f"""
                Dúvida do produtor: "{pergunta}"
                
                Protocolo Ceres MAS:
                1. AVALIAÇÃO DE ESPECIFICIDADE: A pergunta contém cultura e praga/sintoma específicos? 
                   - Se NÃO (ex: só "ajuda com lagarta"): Responda ao produtor explicando que precisa saber qual é a planta e como é a lagarta para não recomendar o remédio errado.
                   - Se SIM: Siga para o passo 2.
                2. PESQUISA: Use a ferramenta 'Consultar Manuais Embrapa'.
                3. RESPOSTA: Formule um plano de ação prático. Se houver dosagem, seja exato.
            """,
            expected_output="Uma interação consultiva (pedido de mais dados) OU um parecer técnico definitivo com fontes.",
            agent=agente
        )

        # 3. Execução
        crew = Crew(
            agents=[agente],
            tasks=[task_consultiva],
            process=Process.sequential,
            verbose=True
        )

        return crew.kickoff()