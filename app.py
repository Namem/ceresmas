import streamlit as st
import os
import sys
import pandas as pd
import plotly.express as px
from sqlalchemy import func

# Garante que o Python encontre a pasta src
sys.path.append(os.path.abspath('.'))

from src.agents.manager import ManagerAgent
from src.database.models import init_db, SessionLocal, CustoProducao

# 1. Configuração da Página Web (Agora mais larga para caber o menu)
st.set_page_config(page_title="Ceres MAS - Assistente", page_icon="🌱", layout="wide")

# 2. Inicialização Segura (Singleton)
@st.cache_resource
def inicializar_sistema():
    """Garante que o banco inicie e o Manager seja criado apenas uma vez por sessão"""
    init_db()
    return ManagerAgent()

manager = inicializar_sistema()

# ==========================================
# 📊 BARRA LATERAL: DASHBOARD FINANCEIRO
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/8920/8920084.png", width=80) # Ícone ilustrativo
    st.header("Análise Financeira")
    st.caption("Visão em tempo real do Custo Operacional Efetivo (COE)")
    
    db = SessionLocal()
    try:
        # Busca os custos agrupados no banco
        custos = db.query(
            CustoProducao.categoria, 
            func.sum(CustoProducao.valor_total)
        ).group_by(CustoProducao.categoria).all()
        
        if custos:
            # Prepara os dados para o Pandas/Plotly
            dados = []
            for cat, valor in custos:
                nome_formatado = cat.name.replace("_", " ").title()
                dados.append({"Categoria": nome_formatado, "Valor (R$)": valor})
            
            df = pd.DataFrame(dados)
            total_geral = df['Valor (R$)'].sum()
            
            # Métrica de Total Destacada
            st.metric(label="Custo Total Acumulado", value=f"R$ {total_geral:,.2f}")
            
            # Gráfico Plotly Elegante
            fig = px.pie(
                df, 
                values='Valor (R$)', 
                names='Categoria', 
                hole=0.5, # Transforma a pizza em "Rosca"
                color_discrete_sequence=px.colors.sequential.Greens_r
            )
            fig.update_layout(
                showlegend=False, # Tira a legenda para economizar espaço
                margin=dict(t=0, b=0, l=0, r=0)
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.info("Nenhum custo registrado na safra atual.")
            
    except Exception as e:
        st.error(f"Erro ao carregar painel: {e}")
    finally:
        db.close()
        
    st.divider()
    st.markdown("**Modo On-Premise** 🟢")
    st.caption("Projeto Ceres MAS - Namem Rachid")

# ==========================================
# 💬 ÁREA PRINCIPAL: CHATBOT (AGRONÔMICO/FINANCEIRO)
# ==========================================
st.title("🌱 Ceres MAS")
st.caption("Converse com seu Engenheiro Agrônomo e Contador Virtual")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá, parceiro! Sou o Ceres. Como posso te ajudar hoje na lavoura ou com as contas?"}
    ]

def montar_historico_texto():
    historico = ""
    for msg in st.session_state.messages[-4:]:
        if msg["role"] == "user":
            historico += f"Produtor: {msg['content']}\n"
        else:
            historico += f"Ceres: {msg['content']}\n"
    return historico

# Renderiza o chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Caixa de Entrada
if prompt := st.chat_input("Ex: Qual remédio para lagarta... ou Comprei 300 reais de semente..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Ceres está analisando os manuais e o cofre..."):
            historico_str = montar_historico_texto()
            try:
                resposta = manager.processar_entrada(prompt, historico_str)
            except Exception as e:
                resposta = f"❌ Ocorreu um erro de comunicação: {e}"
            
            st.markdown(resposta)
    
    st.session_state.messages.append({"role": "assistant", "content": resposta})
    
    # Recarrega a página automaticamente para atualizar o gráfico se houver um novo gasto
    if "FINANCEIRO" in str(resposta).upper() or "SUCESSO" in str(resposta).upper() or "REGISTRAD" in str(resposta).upper():
        st.rerun()