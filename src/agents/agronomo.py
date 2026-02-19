import os
from crewai import Agent, Task, Crew, Process, LLM
from src.tools.rag_tool import RagTools

class AgronomoAgent:
    def executar(self, pergunta: str, historico_chat: str = ""):
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

                agente = Agent(
                    role='Técnico Extensionista Watson (Ceres MAS)',
                    goal='Realizar diagnóstico consultivo e recomendar manejos baseados nos manuais da Embrapa.',
                    backstory="""
                        Você é o Watson, técnico agrícola que atua no Cinturão Verde de Sorriso-MT. 
                        Sua fala é simples e direta (coloquial regional), mas seu embasamento é 100% científico.

                        DIRETRIZES DE COMPORTAMENTO:
                        1. DIAGNÓSTICO ANTES DA PRESCRIÇÃO: Se o produtor disser algo genérico, você NÃO deve dar a solução de imediato. Você deve perguntar: qual a variedade da cultura? Qual o tipo da praga (cor, tamanho)?
                        2. LINGUAJAR: Evite termos excessivamente acadêmicos. Fale "adubação" em vez de "aporte nutricional edáfico".
                        3. RIGOR TÉCNICO: Após entender o problema, cite EXPLICITAMENTE o manual da Embrapa utilizado.
                    """,
                    verbose=True,
                    allow_delegation=False,
                    tools=[RagTools().search_knowledge_base],
                    llm=llm_engine
                )

                task_consultiva = Task(
                    description=f"""
                        Você está no meio de uma conversa com o produtor.
                        
                        HISTÓRICO RECENTE DA CONVERSA:
                        ---
                        {historico_chat}
                        ---

                        MENSAGEM ATUAL DO PRODUTOR: "{pergunta}"
                        
                        Protocolo Ceres MAS (Siga estritamente estes passos):
                        1. SÍNTESE DO PROBLEMA: Una as informações do 'Histórico' com a 'Mensagem Atual'. Qual é a cultura afetada? Qual é a praga ou sintoma?
                        2. AVALIAÇÃO DE ESPECIFICIDADE: Você já possui o nome da planta E as características visuais do problema (cor, tamanho, manchas)?
                           - Se NÃO: Faça uma pergunta amigável e direta pedindo apenas a informação que falta. NÃO dê a solução ainda.
                           - Se SIM: Siga para o passo 3.
                        3. PESQUISA: Se você já tem os detalhes, é OBRIGATÓRIO usar a ferramenta 'Consultar Manuais Embrapa' enviando os termos chave.
                        4. RESPOSTA FINAL: Baseado no texto retornado pela ferramenta, dê a recomendação prática ao produtor citando a fonte oficial.
                    """,
                    expected_output="Uma pergunta pedindo dados faltantes (se incompleto) OU uma recomendação técnica definitiva (se completo).",
                    agent=agente
                )

                crew = Crew(
                    agents=[agente],
                    tasks=[task_consultiva],
                    process=Process.sequential,
                    verbose=True
                )

                # Extrai o texto final e sai do loop
                return crew.kickoff().raw 

            except Exception as e:
                print(f"⚠️ [FALLBACK AGRÔNOMO] Falha no modelo {modelo_atual}. Tentando o próximo... Erro: {str(e)[:50]}")
                continue
        
        return "Puxa parceiro, meus manuais de agronomia estão indisponíveis agora (Sistemas sobrecarregados). Tente de novo em alguns minutos!"