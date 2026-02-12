import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings # <--- MUDANÇA AQUI
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURAÇÃO ---
BASE_DIR = os.getcwd()
DATA_PATH = os.path.join(BASE_DIR, "data", "raw")
DB_PATH = os.path.join(BASE_DIR, "data", "chroma_db")

def ingest_documents():
    """
    Pipeline ETL com Embeddings LOCAIS (HuggingFace).
    Remove a dependência de API externa para a vetorização.
    """
    print("🚀 INICIANDO INGESTÃO COM MODELO LOCAL (OFFLINE)...")
    
    # 1. LIMPEZA
    if os.path.exists(DB_PATH):
        print("🧹 Limpando banco antigo (Google) para substituir pelo Local...")
        shutil.rmtree(DB_PATH)

    # 2. CARREGAMENTO
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Pasta {DATA_PATH} não existe.")
    
    print("📂 Lendo PDFs...")
    loader = PyPDFDirectoryLoader(DATA_PATH)
    raw_documents = loader.load()
    print(f"📄 Páginas: {len(raw_documents)}")

    # 3. CHUNKING
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(raw_documents)
    print(f"🧩 Chunks gerados: {len(chunks)}")

    # 4. VECTORIZATION (LOCAL)
    print("🧠 Baixando/Carregando modelo 'all-MiniLM-L6-v2' (Roda na CPU)...")
    # Este modelo é leve, rápido e gratuito.
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    print(f"⏳ Inserindo {len(chunks)} chunks no ChromaDB (Pode demorar uns minutos)...")
    
    # Como é local, não precisamos de batching/sleep complexo,
    # mas o Chroma gerencia melhor se passarmos tudo de uma vez.
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_PATH
    )
    
    print("\n--------------------------------------------------")
    print(f"✅ SUCESSO! Base vetorial 100% Local criada em: {DB_PATH}")
    print("--------------------------------------------------")

if __name__ == "__main__":
    ingest_documents()