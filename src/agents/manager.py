import os
from crewai import Agent, Task, Crew, Process, LLM
from src.agents.agronomo import AgronomoAgent
from src.agents.financeiro import FinanceiroAgent

class ManagerAgent:
    def processar_entrada(self, entrada_usuario: str, historico_chat: str = ""):
        # LISTA DE FALLBACK (Baseada no painel real do Google AI Studio)
        modelos_fallback = [
            "gemini/gemini-2.5-flash-lite", # 1ª Opção: Rápido e com cota livre (0/20)
            "gemini/gemini-3-flash",        # 2ª Opção: Mais denso, cota livre (0/20)
            "gemini/gemini-2.5-flash"       # 3ª Opção: Esgotado hoje, backup pro futuro
        ]

        classificacao = "GERAL" # Padrão de segurança

        # Loop de Resiliência
        for modelo_atual in modelos_fallback:
            try:
                llm_engine = LLM(
                    model=modelo_atual,
                    api_key=os.getenv("GOOGLE_API_KEY")
                )

                triagem_agent = Agent(
                    role='Gerente de Triagem Ceres',
                    goal='Classificar a demanda do produtor em FINANCEIRO, AGRONOMICO ou GERAL.',
                    backstory='Você é o recepcionista inteligente do sistema. Você não resolve problemas, apenas direciona.',
                    verbose=True,
                    llm=llm_engine,
                    allow_delegation=False
                )

                task_triagem = Task(
                    description=f"""
                    Histórico recente da conversa:
                    {historico_chat}
                    
                    Nova mensagem do produtor: "{entrada_usuario}"
                    
                    Analise a nova mensagem levando em conta o contexto do histórico.
                    Responda APENAS com uma das palavras:
                    - FINANCEIRO (se falar de custos, compras, diesel, valores, dinheiro)
                    - AGRONOMICO (se falar de pragas, doenças, plantio, adubo, bichos ou estiver respondendo uma pergunta técnica anterior)
                    - GERAL (se for 'olá', 'tudo bem' ou fora do contexto)
                    """,
                    expected_output="Uma única palavra classificatória.",
                    agent=triagem_agent
                )

                crew_triagem = Crew(agents=[triagem_agent], tasks=[task_triagem])
                classificacao = crew_triagem.kickoff().raw.strip().upper()
                print(f"\n🚦 [MANAGER] Classificação via {modelo_atual}: {classificacao}")
                break # Se funcionou, sai do loop imediatamente!

            except Exception as e:
                print(f"⚠️ [FALLBACK MANAGER] Falha no modelo {modelo_atual}. Tentando o próximo... Erro: {str(e)[:50]}")
                continue # Pula para o próximo modelo da lista
        else:
            # Se o loop terminar sem dar 'break', todos falharam
            return "Desculpe, meus sistemas de triagem estão sobrecarregados. Pode tentar enviar a mensagem de novo?"

        # Roteamento baseado na classificação
        if "FINANCEIRO" in classificacao:
            return FinanceiroAgent().executar(entrada_usuario)
        elif "AGRONOMICO" in classificacao:
            return AgronomoAgent().executar(entrada_usuario, historico_chat)
        else:
            return "Olá! Sou o Ceres MAS. Posso ajudar com custos da fazenda ou dúvidas técnicas da lavoura."