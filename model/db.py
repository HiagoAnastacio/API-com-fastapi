from typing import Any, Optional, Tuple, List
import mysql.connector as mc #Biblioteca do conector do MySQL
from mysql.connector import Error, MySQLConnection #Importando a classe Error para tratar as mensagens de erro do código
from dotenv import load_dotenv #Importando a função load_dotenv
from os import getenv #Importando a função getenv
 
class Database:
    def __init__(self) -> None:
        load_dotenv()
        self.host: str = getenv('DB_HOST')
        self.username: str = getenv('DB_USER')
        self.password: str = getenv('DB_PSWD')
        self.database: str = getenv('DB_NAME')
        self.connection: Optional[MySQLConnection] = None #Inicialização da conexão
        self.cursor: Optional[List[dict]] = None #Inicialização do cursor
 
    def conectar(self) -> None:
        """Estabelece uma conexão com o banco de dados."""
        try:
            self.connection = mc.connect(
                host = self.host,
                database = self.database,
                user = self.username,
                password = self.password
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                print("Conexão ao banco de dados realizada com sucesso,")
        except Error as e:
            print(f"Erro de conexão: {e}")
            self.connection = None
            self.cursor = None
 
    def desconectar(self) -> None:
        """Encerra a conexão com o banco de dados e o cursor, se eles existirem."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Conexão com o banco de dados encerrada com sucesso;")
   
    def executar_comando(self, sql: str, params: Optional[Tuple[Any, ...]] = None) -> Optional[Optional[List[dict]]]:
        """
        Executa um comando no banco de dados. Pode ser usado para consultas (SELECT) ou modificações (INSERT, UPDATE, DELETE).
        sql: Comando SQL a ser executado.
        params: Parâmetros opcionais para o comando SQL.
        return: Resultados da consulta ou o número de linhas afetadas. Retorna None em caso de erro.
        """
        if self.connection is None:
            print('Conexão ao banco de dados não estabelecida.')
            return None
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(sql, params)
            if sql.strip().lower().startswith("select"):
                resultado = cursor.fetchall()
                return resultado
            else:
                self.connection.commit()
                return cursor.rowcount
        except Error as e:
            print(f'Erro de execução: {e}')
            return None
        finally:
            cursor.close()

    