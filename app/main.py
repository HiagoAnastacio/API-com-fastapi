from fastapi import FastAPI
from typing import Type, List
from model.db import Database
from model.models import BaseModel, Serie, Ator, Motivo, Avaliacao, Categoria
from routes.genericos import rota_delete, rota_get, rota_post, rota_put
from routes import ator_serie
from utils.utils import executar_operacao_db

app = FastAPI()
db = Database()

# Busca todas as tabelas do banco de dados 'mustwatch'
def achar_listar_tabelas(tabelas: List[str]):
    sql = "SELECT `table_name` FROM information_schema.tables WHERE table_schema = 'mustwatch';"
    resultado = executar_operacao_db(sql)
    tabelas = [linha['TABLE_NAME'] for linha in resultado]
    return tabelas

# Cria rotas CRUD para cada tabela informada
def criar_rota_por_tabela(nome_tabela: str, tabelas: List[str], model: Type[BaseModel]):
    for nome_tabela in tabelas:
        rota_get(app, f"/{nome_tabela}", nome_tabela)  # Rota GET (listar)
        rota_post(app, f"/{nome_tabela}", model, nome_tabela)  # Rota POST (criar)
        rota_put(app, f"/{nome_tabela}/{{item_id}}", model, nome_tabela, "id")  # Rota PUT (atualizar)
        rota_delete(app, f"/{nome_tabela}/{{item_id}}", nome_tabela, "id")  # Rota DELETE (deletar)

modelos_por_tabela = {
    "serie": Serie,
    "ator": Ator,
    "motivo_assistir": Motivo,
    "avaliacao_serie": Avaliacao,
    "categoria": Categoria,
}

tabelas = achar_listar_tabelas([])
for tabela in tabelas:
    modelo = modelos_por_tabela.get(tabela, BaseModel)
    criar_rota_por_tabela("", [tabela], modelo)

ator_serie.associar_ator_serie
ator_serie.atualizar_associar_ator_serie
ator_serie.deletar_associacao_ator_serie
ator_serie.listar_serie_e_ator_relacionados
