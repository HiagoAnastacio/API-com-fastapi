from fastapi import FastAPI, HTTPException, status, Query
from model.db import Database
from utils.utils import executar_operacao_db

app = FastAPI()
db = Database()

# Rota GET
@app.get("/ator/{ator_id}/series/", status_code=status.HTTP_200_OK, responses={
    status.HTTP_200_OK: {"description": "Séries encontradas para o ator"},
    status.HTTP_404_NOT_FOUND: {"description": "Nenhuma série encontrada para o ator especificado"},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Erro interno do servidor"}
})
def listar_serie_e_ator_relacionados(ator_id: int,  serie_id: int):
    """
    Lista todas as séries associadas a um ator específico.
    """
    sql = """
        SELECT s.serie_id, s.titulo_serie, s.descricao, s.ano_lancamento
        FROM serie s
        JOIN ator_serie AS `as` ON s.serie_id = `as`.serie_id -- Use alias para evitar conflito com 'as' keyword
        WHERE `as`.ator_id = %s
    """
    resultado = executar_operacao_db(sql, (ator_id, serie_id))
   
    if resultado:
        return resultado
    # Se não houver resultado, levanta 404 (Nenhum item encontrado)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Nenhuma série encontrada para o ator ID {ator_id}.")
 
#Rota POST
@app.post("/ator/{ator_id}/series/{serie_id}", status_code=status.HTTP_201_CREATED, responses={
    status.HTTP_201_CREATED: {"description": "Associação entre ator e série criada com sucesso"},
    status.HTTP_400_BAD_REQUEST: {"description": "Associação já existe ou dados inválidos"},
    status.HTTP_404_NOT_FOUND: {"description": "ator ou série não encontrado"},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Erro interno do servidor"}
})
def associar_ator_serie(ator_id: int, serie_id: int):
    """
    Associa uma série a um ator.
    """
    # 1. Verifica se o ator existe
    sql_ator = "SELECT COUNT(*) FROM ator WHERE ator_id = %s"
    ator_count_result = executar_operacao_db(sql_ator, (ator_id,))
    if not ator_count_result or ator_count_result[0]['COUNT(*)'] == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ator com ID {ator_id} não encontrado.")
   
    # 2. Verifica se a série existe
    sql_serie = "SELECT COUNT(*) FROM serie WHERE serie_id = %s"
    sql_serie_exis = executar_operacao_db(sql_serie, (serie_id,))
    if not sql_serie_exis or sql_serie_exis[0]['COUNT(*)'] == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Série com ID {serie_id} não encontrada.")
   
    # 3. Verifica se a associação já existe para evitar duplicatas
    sql_exis_associacao = "SELECT COUNT(*) FROM ator_serie WHERE ator_id = %s AND serie_id = %s"
    resultado_associacao_exis = executar_operacao_db(sql_exis_associacao, (ator_id, serie_id))
    if resultado_associacao_exis and resultado_associacao_exis[0]['COUNT(*)'] > 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Associação entre este ator e série já existe.") # 409 Conflict para duplicidade
   
    # 4. Se tudo OK, insere a associação
    sql_insert = "INSERT INTO ator_serie (ator_id, serie_id) VALUES (%s, %s)"
    executar_operacao_db(sql_insert, (ator_id, serie_id))
 
    return {"saída": f"Associação entre ator ID {ator_id} e série ID {serie_id} criada com sucesso!"}
 
#Rota UPDATE
@app.put("/ator/{ator_id}/series/{serie_id}", status_code=status.HTTP_201_CREATED, responses={
    status.HTTP_201_CREATED: {"description": "Associação entre ator e série criada com sucesso"},
    status.HTTP_400_BAD_REQUEST: {"description": "Associação já existe ou dados inválidos"},
    status.HTTP_404_NOT_FOUND: {"description": "ator ou série não encontrado"},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Erro interno do servidor"}
})
def atualizar_associar_ator_serie(ator_id: int, serie_id: int):
    """
    Atualiza a associação entre ator e série (exemplo: trocar a série associada a um ator).
    Para este exemplo, vamos supor que queremos atualizar a série associada a um ator para uma nova série.
    """
    # Verifica se a associação existe
    sql_exis_associacao = "SELECT COUNT(*) FROM ator_serie WHERE ator_id = %s AND serie_id = %s"
    resultado_associacao_exis = executar_operacao_db(sql_exis_associacao, (ator_id, serie_id))
    if not resultado_associacao_exis or resultado_associacao_exis[0]['COUNT(*)'] == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associação entre este ator e série não existe.")
 
    # Exemplo: atualizar para uma nova série (novo_serie_id passado como query param ou body, aqui usaremos query param)
    def inner_update(novo_serie_id: int = Query(..., description="Novo ID da série para atualizar a associação")):
        # Verifica se a nova série existe
        sql_serie = "SELECT COUNT(*) FROM serie WHERE serie_id = %s"
        sql_serie_exis = executar_operacao_db(sql_serie, (novo_serie_id,))
        if not sql_serie_exis or sql_serie_exis[0]['COUNT(*)'] == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Série com ID {novo_serie_id} não encontrada.")
 
        # Atualiza a associação
        sql_update = "UPDATE ator_serie SET serie_id = %s WHERE ator_id = %s AND serie_id = %s"
        executar_operacao_db(sql_update, (novo_serie_id, ator_id, serie_id))
        return {"saída": f"Associação do ator ID {ator_id} atualizada para série ID {novo_serie_id} com sucesso!"}
    return inner_update
 
#Rota DELETE
@app.delete("/ator/{ator_id}/series/{serie_id}", status_code=status.HTTP_200_OK, responses={
    status.HTTP_200_OK: {"description": "Associação entre ator e série removida com sucesso"},
    status.HTTP_404_NOT_FOUND: {"description": "Associação não encontrada"},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Erro interno do servidor"}
})
def deletar_associacao_ator_serie(ator_id: int, serie_id: int):
    """
    Remove a associação entre um ator e uma série.
    """
    # Verifica se a associação existe
    sql_exis_associacao = "SELECT COUNT(*) FROM ator_serie WHERE ator_id = %s AND serie_id = %s"
    resultado_associacao_exis = executar_operacao_db(sql_exis_associacao, (ator_id, serie_id))
    if not resultado_associacao_exis or resultado_associacao_exis[0]['COUNT(*)'] == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associação entre este ator e série não existe.")
 
    sql_delete = "DELETE FROM ator_serie WHERE ator_id = %s AND serie_id = %s"
    executar_operacao_db(sql_delete, (ator_id, serie_id))
    return {"saída": f"Associação entre ator ID {ator_id} e série ID {serie_id} removida com sucesso!"}
