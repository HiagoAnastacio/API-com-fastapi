from typing import Optional
from pydantic import BaseModel 

class serie(BaseModel):
    titulo: str
    descricao: Optional[str]
    ano_lancamento: Optional[int]
    id_categoria: int

class autor(BaseModel):
    nome_autor: str

class motivo_assistir(BaseModel):
    id_serie: int
    motivo: str

class avaliacao_serie(BaseModel):
    id_serie: int
    nota: int
    comentario: Optional[str]

class categoria(BaseModel):
    nome_categoria: str