from src.database.models import SessionLocal, CustoProducao

def consultar_extrato():
    # 1. Abre a conexão com o PostgreSQL
    db = SessionLocal()
    
    try:
        # 2. Faz um SELECT * FROM custos_producao
        custos = db.query(CustoProducao).all()
        
        print("\n📊 --- EXTRATO FINANCEIRO (POSTGRESQL) ---")
        
        if not custos:
            print("Nenhum custo registrado no banco de dados.")
        else:
            for custo in custos:
                print(f"ID: {custo.id}")
                print(f"Categoria: {custo.categoria.name}")
                print(f"Descrição: {custo.descricao}")
                print(f"Valor Total: R$ {custo.valor_total:.2f}")
                print(f"Data: {custo.data_gasto.strftime('%d/%m/%Y %H:%M')}")
                print("-" * 45)
                
    except Exception as e:
        print(f"❌ Erro ao consultar o banco: {e}")
    finally:
        # 3. Fecha a conexão
        db.close()

if __name__ == "__main__":
    consultar_extrato()