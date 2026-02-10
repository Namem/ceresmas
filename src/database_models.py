import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime
import enum

# --- CONFIGURAÇÃO ---
# String de conexão: driver://usuario:senha@host:porta/nome_banco
# Nota: Como estamos rodando o script DO WINDOWS (fora do docker) apontando para o Docker, usamos 'localhost'
DATABASE_URL = "postgresql://admin:admin123@localhost:5432/ceres_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- ENUMS (Padronização) ---
class TipoTransacao(enum.Enum):
    RECEITA = "receita"
    DESPESA = "despesa"

class CategoriaCusto(enum.Enum):
    INSUMO_SEMENTE = "sementes"
    INSUMO_FERTILIZANTE = "fertilizantes"
    INSUMO_DEFENSIVO = "defensivos"
    OPERACIONAL_COMBUSTIVEL = "combustivel"
    OPERACIONAL_MANUTENCAO = "manutencao"
    MAO_DE_OBRA = "mao_de_obra"
    OUTROS = "outros"

class StatusCiclo(enum.Enum):
    PLANEJAMENTO = "planejamento"
    PLANTIO = "plantio"
    VEGETATIVO = "vegetativo"
    COLHEITA = "colheita"
    FINALIZADO = "finalizado"

# --- TABELAS ---

class Produtor(Base):
    __tablename__ = 'produtores'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True)
    # Relação 1-para-Muitos
    propriedades = relationship("Propriedade", back_populates="produtor")
    

class Propriedade(Base):
    __tablename__ = 'propriedades'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    localizacao = Column(String)
    area_total = Column(Float)
    produtor_id = Column(Integer, ForeignKey('produtores.id'))
    
    produtor = relationship("Produtor", back_populates="propriedades")
    talhoes = relationship("Talhao", back_populates="propriedade")

class Talhao(Base):
    __tablename__ = 'talhoes'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String) # Ex: "Talhão da Represa"
    area_hectares = Column(Float)
    propriedade_id = Column(Integer, ForeignKey('propriedades.id'))
    
    propriedade = relationship("Propriedade", back_populates="talhoes")
    ciclos = relationship("CicloSafra", back_populates="talhao")

class CicloSafra(Base):
    __tablename__ = 'ciclos_safra'
    
    id = Column(Integer, primary_key=True, index=True)
    cultura = Column(String) # Ex: "Soja Intacta"
    data_inicio = Column(DateTime, default=datetime.now)
    data_previsao_colheita = Column(DateTime)
    status = Column(Enum(StatusCiclo), default=StatusCiclo.PLANEJAMENTO)
    
    talhao_id = Column(Integer, ForeignKey('talhoes.id'))
    talhao = relationship("Talhao", back_populates="ciclos")
    custos = relationship("CustoProducao", back_populates="ciclo")

class CustoProducao(Base):
    """
    Tabela Fato: A 'Caixa Preta' financeira.
    """
    __tablename__ = 'custos_producao'
    
    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=False) # Texto cru, ex: "Comprei 30 sacos de ureia"
    valor_total = Column(Float, nullable=False)
    quantidade = Column(Float, nullable=True) # Ex: 30.0
    unidade = Column(String, nullable=True)   # Ex: "sacos"
    categoria = Column(Enum(CategoriaCusto), nullable=False)
    data_gasto = Column(DateTime, default=datetime.now)
    
    ciclo_id = Column(Integer, ForeignKey('ciclos_safra.id'))
    ciclo = relationship("CicloSafra", back_populates="custos")

# --- EXECUÇÃO ---
def init_db():
    print("⏳ Conectando ao Docker Postgres...")
    try:
        # Cria todas as tabelas definidas acima
        Base.metadata.create_all(bind=engine)
        print("✅ Sucesso! Tabelas criadas no banco 'Ceres Mas'.")
    except Exception as e:
        print(f"❌ Erro ao conectar no Docker: {e}")
        print("Dica: Verifique se rodou 'docker compose up -d'")

if __name__ == "__main__":
    init_db()