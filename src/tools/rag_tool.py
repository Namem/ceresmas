import os
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from crewai.tools import tool

# Caminho para o banco de dados (mesmo do script de ingestão)
BASE_DIR = os.getcwd()
DB_PATH = os.path.join(BASE_DIR, "data", "chroma_db")

class RagTools:
    @tool("Consultar Manuais Embrapa")
    def search_knowledge_base(query: str):
        """
        Utilize esta ferramenta para buscar informações técnicas sobre:
        - Pragas e doenças de hortaliças (tomate, alface, etc).
        - Manejo, adubação e clima.
        - Dados técnicos da Embrapa.
        Entrada: Uma pergunta específica ou termo de busca (ex: "Como controlar lagarta do tomate").
        """
        # Verifica se o banco existe
        if not os.path.exists(DB_PATH):
            return "Erro: A base de conhecimento não foi encontrada. Rode o script de ingestão primeiro."

        # Conecta ao banco existente
        embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
        
        # Busca os 3 trechos mais relevantes
        results = db.similarity_search(query, k=3)
        
        # Compila a resposta
        context = "\n\n".join([doc.page_content for doc in results])
        return f"FONTES OFICIAIS EMBRAPA ENCONTRADAS:\n{context}"