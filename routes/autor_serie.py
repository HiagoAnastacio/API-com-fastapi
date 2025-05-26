from fastapi import APIRouter, HTTPException, status
from model.db import Database
from utils.funcao_execucao import executar_operacao_db

router = APIRouter()
db = Database() 

# Rotas associativas
# ==============================================================================================================
# Rota GET ⬇
# ==============================================================================================================
@router.get("/autor/{autor_id}/series/", status_code=status.HTTP_200_OK, responses={
    status.HTTP_200_OK: {"description": "Séries encontradas para o autor"},
    status.HTTP_404_NOT_FOUND: {"description": "Nenhuma série encontrada para o autor especificado"},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Erro interno do servidor"}
})
def listar_serie_e_autor_relacionados():
    """
    Lista todas as séries associadas a um autor específico.
    """
    sql = """
        SELECT * FROM autor_serie;
        """
    resultado = executar_operacao_db(sql)
    if resultado:
        return resultado
    # Se não houver resultado, levanta 404 (Nenhum item encontrado)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhuma série encontrada para associação.")

# ==============================================================================================================
# Rota POST ⬇
# ==============================================================================================================
@router.post("/autor/{autor_id}/series/{serie_id}", status_code=status.HTTP_201_CREATED, responses={
    status.HTTP_201_CREATED: {"description": "Associação entre autor e série criada com sucesso"},
    status.HTTP_400_BAD_REQUEST: {"description": "Associação já existe ou dados inválidos"},
    status.HTTP_404_NOT_FOUND: {"description": "Autor ou série não encontrado"},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Erro interno do servidor"}
})
def associar_autor_serie(autor_id: int, serie_id: int):
    """
    Associa uma série a um autor.
    """
    # Se tudo OK, insere a associação
    sql_insert = "INSERT INTO autor_serie (autor_id, serie_id) VALUES (%s, %s)"
    executar_operacao_db(sql_insert, (autor_id, serie_id)) 

    # Retorno conforme suas rotas genéricas para consistência
    return {"saída": f"Associação entre autor ID {autor_id} e série ID {serie_id} criada com sucesso!"}

# ==============================================================================================================
# Rota UPDATE ⬇
# ==============================================================================================================
@router.put("/autor/{autor_id}/series/{serie_id}", status_code=status.HTTP_201_CREATED, responses={
    status.HTTP_201_CREATED: {"description": "Associação entre autor e série criada com sucesso"},
    status.HTTP_400_BAD_REQUEST: {"description": "Associação já existe ou dados inválidos"},
    status.HTTP_404_NOT_FOUND: {"description": "Autor ou série não encontrado"},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Erro interno do servidor"}
})
def atualizar_associar_autor_serie(autor_serie_id: int, novo_autor_id: int, novo_serie_id: int):
    """
    Atualiza a associação entre autor e série (exemplo: trocar a série associada a um autor).
    Para este exemplo, vamos supor que queremos atualizar a série associada a um autor para uma nova série.
    """
    # O usuário deve informar o autor_serie_id que será alterado, além dos novos autor_id e serie_id
    sql_update = "UPDATE autor_serie SET autor_id = %s, serie_id = %s WHERE autor_serie_id = %s"
    executar_operacao_db(sql_update, (novo_autor_id, novo_serie_id, autor_serie_id))
    return {"saída": f"Associação {autor_serie_id} atualizada para autor ID {novo_autor_id} e série ID {novo_serie_id} com sucesso!"}

# ==============================================================================================================
# Rota DELETE ⬇
# ==============================================================================================================
@router.delete("/autor/{autor_id}/series/{serie_id}", status_code=status.HTTP_200_OK, responses={
    status.HTTP_200_OK: {"description": "Associação entre autor e série removida com sucesso"},
    status.HTTP_404_NOT_FOUND: {"description": "Associação não encontrada"},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Erro interno do servidor"}
})
def deletar_associacao_autor_serie(autor_id: int, serie_id: int):
    """
    Remove a associação entre um autor e uma série.
    """

    # Remove a associação
    sql_delete = "DELETE FROM autor_serie WHERE autor_id = %s AND serie_id = %s"
    executar_operacao_db(sql_delete, (autor_id, serie_id))
    return {"saída": f"Associação entre autor ID {autor_id} e série ID {serie_id} removida com sucesso!"}
