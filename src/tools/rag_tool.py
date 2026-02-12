import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings # <--- MUDANÇA AQUI
from crewai.tools import tool

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
        """
        if not os.path.exists(DB_PATH):
            return "Erro: Base de conhecimento não encontrada."

        # ATENÇÃO: O modelo aqui deve ser IGUAL ao da ingestão
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
        
        # Busca
        results = db.similarity_search(query, k=3)
        context = "\n\n".join([doc.page_content for doc in results])
        
        return f"FONTES OFICIAIS EMBRAPA (Model Local):\n{context}"