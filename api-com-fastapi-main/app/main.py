from fastapi import FastAPI, HTTPException
from typing import Type, List
from model.db import Database
from model.models import BaseModel

app = FastAPI()
db = Database()

def executar_operacao_db(sql: str, params: tuple = None):
    try:
        db.conectar()
        resultado = db.executar_comando(sql, params)
        db.desconectar()
        return resultado
    except Exception as e:
        db.desconectar()
        raise HTTPException(status_code=500, detail=str(e))

def achar_listar_tabelas(tabelas: List[str]):
    sql = "SELECT `table_name` FROM information_schema.tables WHERE table_schema = 'mustwatch';"
    resultado = executar_operacao_db(sql)
    tabelas = [linha['TABLE_NAME'] for linha in resultado]
    return tabelas

def criar_rota_por_tabela(nome_tabela: str, tabelas: List[str], model: Type[BaseModel]):
    for nome_tabela in tabelas:
        rota_get(app, f"/{nome_tabela}", nome_tabela)
        rota_post(app, f"/{nome_tabela}", model, nome_tabela)
        rota_update(app, f"/{nome_tabela}/{{item_id}}", model, nome_tabela, "id")
        rota_delete(app, f"/{nome_tabela}/{{item_id}}", nome_tabela, "id")

def rota_get(app: FastAPI, txtAncor: str, nome_tabela: str):
    @app.get(txtAncor, status_code=200, responses={
        200: {"description": "Itens encontrados"},
        404: {"description": "Nenhum item encontrado"},
        500: {"description": "Erro interno do servidor"}
    })
    def listar_itens():
        sql = f"SELECT * FROM {nome_tabela}"
        resultado = executar_operacao_db(sql)
        if resultado:
            return resultado
        raise HTTPException(status_code=404, detail="Nenhum item encontrado")
    return listar_itens

def rota_post(app: FastAPI, txtAncor: str, model: Type[BaseModel], nome_tabela: str):
    @app.post(txtAncor, status_code=201, responses={
        201: {"description": "Item criado com sucesso"},
        422: {"description": "Erro de validação"},
        500: {"description": "Erro interno do servidor"}
    })
    def criar_item(item: model): # type: ignore
        try:
            campos = ", ".join(item.dict().keys())
            valores = ", ".join(["%s"] * len(item.dict()))
            sql = f"INSERT INTO {nome_tabela} ({campos}) VALUES ({valores})"
            executar_operacao_db(sql, tuple(item.dict().values()))
            return {"saída": f"{nome_tabela[:-1].capitalize()} cadastrado com sucesso"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    return criar_item

def rota_update(app: FastAPI, txtAncor: str, model: Type[BaseModel], nome_tabela: str, id_pk: str):
    @app.put(txtAncor, status_code=200, responses={
        200: {"description": "Item atualizado com sucesso"},
        404: {"description": "Item não encontrado"},
        422: {"description": "Erro de validação"},
        500: {"description": "Erro interno do servidor"}
    })
    def atualizar_item(item_id: int, item: model): # type: ignore
        updates = ", ".join([f"{key} = %s" for key in item.dict().keys()])
        sql = f"UPDATE {nome_tabela} SET {updates} WHERE {id_pk} = %s"
        resultado = executar_operacao_db(sql, tuple(list(item.dict().values()) + [item_id]))
        if resultado == 0:
            raise HTTPException(status_code=404, detail="Item não encontrado")
        return {"saída": f"{nome_tabela[:-1].capitalize()} atualizado com sucesso"}
    return atualizar_item

def rota_delete(app: FastAPI, txtAncor: str, nome_tabela: str, id_pk: str):
    @app.delete(txtAncor, status_code=200, responses={
        200: {"description": "Item deletado com sucesso"},
        404: {"description": "Item não encontrado"},
        500: {"description": "Erro interno do servidor"}
    })
    def deletar_item(item_id: int):
        sql = f"DELETE FROM {nome_tabela} WHERE {id_pk} = %s"
        resultado = executar_operacao_db(sql, (item_id,))
        if resultado == 0:
            raise HTTPException(status_code=404, detail="Item não encontrado")
        return {"saída": f"{nome_tabela[:-1].capitalize()} deletado com sucesso"}
    return deletar_item

tabelas = achar_listar_tabelas([])
criar_rota_por_tabela("", tabelas, BaseModel)