from fastapi import FastAPI, HTTPException
from utils.utils import executar_operacao_db
from typing import Type
from pydantic import BaseModel

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

# Cria rota POST para inserir um novo item na tabela
def rota_post(app: FastAPI, txtAncor: str, model: Type[BaseModel], nome_tabela: str):
    @app.post(txtAncor, status_code=201, responses={
        201: {"description": "Item criado com sucesso"},
        422: {"description": "Erro de validação"},
        500: {"description": "Erro interno do servidor"}
    })
    def criar_item(item: model): # type: ignore
        try:
            campos = ", ".join(item.dict().keys())  # Campos da tabela
            valores = ", ".join(["%s"] * len(item.dict()))  # Placeholders para os valores
            sql = f"INSERT INTO {nome_tabela} ({campos}) VALUES ({valores})"
            executar_operacao_db(sql, tuple(item.dict().values()))
            return {"saída": f"{nome_tabela} cadastrado com sucesso"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    return criar_item

# Cria rota PUT para atualizar um item existente na tabela
def rota_put(app: FastAPI, txtAncor: str, model: Type[BaseModel], nome_tabela: str, id_pk: str):
    @app.put(txtAncor, status_code=200, responses={
        200: {"description": "Item atualizado com sucesso"},
        404: {"description": "Item não encontrado"},
        422: {"description": "Erro de validação"},
        500: {"description": "Erro interno do servidor"}
    })
    def atualizar_item(item_id: int, item: model): # type: ignore
        updates = ", ".join([f"{key} = %s" for key in item.dict().keys()])  # Monta SET do UPDATE
        sql = f"UPDATE {nome_tabela} SET {updates} WHERE {id_pk} = %s"
        resultado = executar_operacao_db(sql, tuple(list(item.dict().values()) + [item_id]))
        if resultado == 0:
            raise HTTPException(status_code=404, detail="Item não encontrado")
        return {"saída": f"{nome_tabela} atualizado com sucesso"}
    return atualizar_item

# Cria rota DELETE para remover um item da tabela
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
        return {"saída": f"{nome_tabela} deletado com sucesso"}
    return deletar_item
