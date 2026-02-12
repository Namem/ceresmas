import google.generativeai as genai
import os
from dotenv import load_dotenv

# Carrega ambiente
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ ERRO: Chave API não encontrada no arquivo .env")
    exit()

# Configura a API
genai.configure(api_key=api_key)

print("🔍 CONSULTANDO API DO GOOGLE PARA LISTAR MODELOS DISPONÍVEIS...")
print("-" * 50)

try:
    found = False
    for m in genai.list_models():
        # Filtra apenas modelos que fazem "embedContent" (o que precisamos)
        if 'embedContent' in m.supported_generation_methods:
            print(f"✅ MODELO DE EMBEDDING ENCONTRADO: {m.name}")
            found = True
    
    if not found:
        print("⚠️  Nenhum modelo de embedding encontrado. Verifique se a API 'Generative Language API' está habilitada no Google Cloud Console.")

except Exception as e:
    print(f"❌ ERRO DE CONEXÃO: {e}")

print("-" * 50)