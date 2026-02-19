import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from crewai.tools import tool

BASE_DIR = os.getcwd()
DB_PATH = os.path.join(BASE_DIR, "data", "chroma_db")

class RagTools:
    @tool("Consultar Manuais Embrapa")
    def search_knowledge_base(query: str):
        """
        Utilize esta ferramenta para buscar informações técnicas sobre:
        - Pragas e doenças de hortaliças.
        - Manejo, adubação e clima.
        Use termos específicos na busca (ex: "controle lagarta helicoverpa tomate").
        """
        if not os.path.exists(DB_PATH):
            return "Erro: Base de conhecimento não encontrada. Execute o ingest_pdf.py."

        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
        
        # MUDANÇA CRÍTICA: search_type="mmr" e k=5 para mais contexto
        # fetch_k=10 busca 10 candidatos e seleciona os 5 mais diversos
        retriever = db.as_retriever(
            search_type="mmr", 
            search_kwargs={"k": 5, "fetch_k": 10, "lambda_mult": 0.5} 
        )
        
        docs = retriever.invoke(query)
        context = "\n---\n".join([doc.page_content for doc in docs])
        
        return f"FONTES OFICIAIS EMBRAPA (RAG Local MMR):\n{context}"