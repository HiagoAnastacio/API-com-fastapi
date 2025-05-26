from fastapi import FastAPI, HTTPException
from model.db import Database

# Instancia o aplicativo FastAPI e o banco de dados
app = FastAPI()
db = Database()

# Função utilitária para executar comandos no banco de dados com tratamento de exceções
def executar_operacao_db(sql: str, params: tuple = None):
    try:
        db.conectar()  # Abre conexão
        resultado = db.executar_comando(sql, params)  # Executa comando SQL
        db.desconectar()  # Fecha conexão
        return resultado
    except Exception as e:
        db.desconectar()
        raise HTTPException(status_code=500, detail=str(e))