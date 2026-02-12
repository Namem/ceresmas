import os
import shutil
import time
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# --- CONFIGURAÇÃO DE CAMINHOS ---
BASE_DIR = os.getcwd()
DATA_PATH = os.path.join(BASE_DIR, "data", "raw")
DB_PATH = os.path.join(BASE_DIR, "data", "chroma_db")

def ingest_documents():
    """
    Executa o pipeline ETL com Throttling (Controle de Taxa) para respeitar
    os limites da API gratuita do Google Gemini.
    """
    print("🚀 INICIANDO INGESTÃO COM CONTROLE DE TAXA (RATE LIMIT)...")
    
    # 1. VALIDAÇÃO E LIMPEZA
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"❌ ERRO: Pasta {DATA_PATH} não encontrada.")
    
    if os.path.exists(DB_PATH):
        print("🧹 Limpando banco antigo...")
        shutil.rmtree(DB_PATH)

    # 2. EXTRACT
    print("📂 Carregando PDFs...")
    loader = PyPDFDirectoryLoader(DATA_PATH)
    raw_documents = loader.load()
    print(f"📄 Páginas carregadas: {len(raw_documents)}")

    # 3. TRANSFORM
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(raw_documents)
    print(f"🧩 Total de chunks para processar: {len(chunks)}")

    # 4. LOAD (COM BATCHING)
    print("🧠 Inicializando modelo de Embeddings...")
    # ATENÇÃO: Usando o modelo validado no seu diagnóstico
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    
    # Inicializa o banco vazio
    vector_store = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embeddings
    )

    BATCH_SIZE = 20  # Envia 20 chunks por vez
    SLEEP_TIME = 2   # Espera 2 segundos entre lotes
    
    print(f"⏳ Iniciando inserção em lotes de {BATCH_SIZE}...")
    
    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i : i + BATCH_SIZE]
        print(f"   Processando lote {i}/{len(chunks)}...", end="\r")
        
        try:
            vector_store.add_documents(batch)
            time.sleep(SLEEP_TIME) # Pausa para não estourar a cota
            
        except Exception as e:
            if "429" in str(e):
                print(f"\n⚠️  Rate Limit atingido no lote {i}. Esperando 60s para esfriar...")
                time.sleep(60) # Backoff agressivo
                vector_store.add_documents(batch) # Tenta novamente
                print("   ✅ Retomando...")
            else:
                print(f"\n❌ Erro desconhecido no lote {i}: {e}")

    print("\n--------------------------------------------------")
    print(f"✅ SUCESSO! Todos os {len(chunks)} chunks foram indexados.")
    print(f"📁 Banco salvo em: {DB_PATH}")
    print("--------------------------------------------------")

if __name__ == "__main__":
    ingest_documents()