from crewai.tools import tool
from sqlalchemy.orm import Session
from src.database.models import engine, CustoProducao, CategoriaCusto, CicloSafra
from datetime import datetime


class FerramentasFinanceiras:
    
    @tool("Registrar Custo de Produção")
    def registrar_custo(descricao: str, valor: float, categoria: str, quantidade: float = 0, unidade: str = None):
        """
        Registra um custo financeiro no banco de dados do Ceres MAS.
        
        Parâmetros:
        - descricao: Detalhe do gasto (ex: 'Compra de Adubo NPK').
        - valor: Valor monetário total (float).
        - categoria: Deve ser uma dessas: ['sementes', 'fertilizantes', 'defensivos', 'combustivel', 'manutencao', 'mao_de_obra', 'outros']
        - quantidade: (Opcional) Quantidade física.
        - unidade: (Opcional) kg, litros, sacos.
        """
        
        session = Session(bind=engine)
        try:
            # 1. Busca o ciclo ativo (Hardcoded ID=1 para o TCC)
            ciclo_ativo = session.query(CicloSafra).filter_by(id=1).first()
            
            if not ciclo_ativo:
                return "Erro: Não há safra ativa (ID 1) cadastrada."

            # 2. Converte a string do LLM para o Enum do Banco
            mapa_categorias = {
                "sementes": CategoriaCusto.INSUMO_SEMENTE,
                "fertilizantes": CategoriaCusto.INSUMO_FERTILIZANTE,
                "adubo": CategoriaCusto.INSUMO_FERTILIZANTE,
                "defensivos": CategoriaCusto.INSUMO_DEFENSIVO,
                "veneno": CategoriaCusto.INSUMO_DEFENSIVO,
                "combustivel": CategoriaCusto.OPERACIONAL_COMBUSTIVEL,
                "diesel": CategoriaCusto.OPERACIONAL_COMBUSTIVEL,
                "manutencao": CategoriaCusto.OPERACIONAL_MANUTENCAO,
                "mao_de_obra": CategoriaCusto.MAO_DE_OBRA
            }
            # Se o LLM mandar algo estranho, cai em OUTROS
            categoria_enum = mapa_categorias.get(categoria.lower(), CategoriaCusto.OUTROS)

            # 3. Insere no Banco
            novo_custo = CustoProducao(
                descricao=descricao,
                valor_total=valor,
                quantidade=quantidade,
                unidade=unidade,
                categoria=categoria_enum,
                ciclo_id=ciclo_ativo.id,
                data_gasto=datetime.now()
            )
            
            session.add(novo_custo)
            session.commit()
            
            return f"✅ SUCESSO SQL: Custo '{descricao}' de R$ {valor} registrado na categoria '{categoria_enum.name}'."
            
        except Exception as e:
            session.rollback()
            return f"❌ ERRO SQL: {str(e)}"
        finally:
            session.close()