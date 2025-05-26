from fastapi import FastAPI, HTTPException
from model.db import Database

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