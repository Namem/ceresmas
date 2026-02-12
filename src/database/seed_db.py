from sqlalchemy.orm import Session
from src.database.models import engine, Produtor, Propriedade, Talhao, CicloSafra, StatusCiclo, Base

def popular_banco():
    # Cria uma sessão temporária
    session = Session(bind=engine)
    
    print("🌱 Iniciando a plantação de dados (Seeding)...")

    # 1. Verifica se já existe dados para não duplicar
    if session.query(Produtor).first():
        print("⚠️ O banco já possui dados. Pulando o seed.")
        return

    # 2. Cria o Produtor (Persona do TCC)
    produtor = Produtor(nome="Namem Rachid", email="namem@ceres.ag")
    session.add(produtor)
    session.commit() # Salva para gerar o ID

    # 3. Cria a Propriedade
    fazenda = Propriedade(
        nome="Fazenda Santa Fé",
        localizacao="Cuiabá - MT",
        area_total=1500.0,
        produtor_id=produtor.id
    )
    session.add(fazenda)
    session.commit()

    # 4. Cria um Talhão
    talhao_01 = Talhao(
        nome="Talhão da Represa (T01)",
        area_hectares=100.0,
        propriedade_id=fazenda.id
    )
    session.add(talhao_01)
    session.commit()

    # 5. Cria o Ciclo Atual (Safra 24/25)
    ciclo_soja = CicloSafra(
        cultura="Soja Intacta",
        status=StatusCiclo.VEGETATIVO,
        talhao_id=talhao_01.id
    )
    session.add(ciclo_soja)
    session.commit()

    print(f"✅ Dados criados com sucesso!")
    print(f"   👨‍🌾 Produtor: {produtor.nome} (ID: {produtor.id})")
    print(f"   🚜 Fazenda: {fazenda.nome}")
    print(f"   🌱 Ciclo Ativo: {ciclo_soja.cultura} (ID: {ciclo_soja.id})")

if __name__ == "__main__":
    popular_banco()