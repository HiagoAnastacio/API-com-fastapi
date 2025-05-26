from fastapi import FastAPI
from typing import Type, List
from model.db import Database
from utils.funcao_execucao import executar_operacao_db
from routes import autor_serie
from routes.genericas import rota_get, rota_post, rota_put, rota_delete
from routes.autor_serie import router as autor_serie_router
from model.models import BaseModel, serie, autor, categoria,avaliacao_serie, motivo_assistir

app = FastAPI()
app.include_router(autor_serie_router)
db = Database()

def achar_listar_tabelas(tabelas: List[str]):
    sql = "SELECT `table_name` FROM information_schema.tables WHERE table_schema = 'mustwatch';"
    resultado = executar_operacao_db(sql)
    tabelas = [linha['TABLE_NAME'] for linha in resultado]
    return tabelas

def criar_rota_por_tabela(nome_tabela: str, tabelas: List[str], model: Type[BaseModel]):
    for nome_tabela in tabelas:
        rota_get(app, f"/{nome_tabela}", nome_tabela)
        rota_post(app, f"/{nome_tabela}", model, nome_tabela)
        rota_put(app, f"/{nome_tabela}/{{item_id}}", model, nome_tabela, f"{nome_tabela}_id") # Atualiza o item com id_pk cujo o nome da coluna seja igual ao nome da tabela + "_id"
        rota_delete(app, f"/{nome_tabela}/{{item_id}}", nome_tabela, f"{nome_tabela}_id")

# Rotas associativas
autor_serie.listar_serie_e_autor_relacionados
autor_serie.associar_autor_serie
autor_serie.atualizar_associar_autor_serie
autor_serie.deletar_associacao_autor_serie

modelos_por_tabela = {
    "serie": serie,
    "autor": autor,
    "motivo_assistir": motivo_assistir,
    "avaliacao": avaliacao_serie,
    "categoria": categoria,
}
 
tabelas = achar_listar_tabelas([])
for tabela in tabelas:
    modelo = modelos_por_tabela.get(tabela, BaseModel)
    criar_rota_por_tabela("", [tabela], modelo)
 