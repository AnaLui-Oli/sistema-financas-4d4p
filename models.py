from sqlmodel import SQLModel as model, Field, create_engine, Relationship
from enum import Enum
from datetime import date

#nomeando o banco

schema_name = "sistema_bancario.db"
sql_url = f"sqlite:///{schema_name}"

#modelos

class Bancos(Enum):
    NUBANK ="Nubank"
    INTER = "Inter"
    CAIXA = "Caixa"
    ITAU = "Itaú"
    SANTANDER = "Santander"
    BANCO_BRASIL = "Banco do Brasil"

class Status(Enum):
    ATIVO = "Ativo"
    INATIVO = "Inativo"

class Conta(model ,table=True):
    id: int = Field(primary_key=True)
    user: str
    saldo: float
    banco: Bancos = Field(default=Bancos.NUBANK)
    status: Status = Field(default=Status.ATIVO)

class Tipos(Enum):
    SAIDA = "Saida"
    ENTRADA = "Entrada"

class Historico(model, table=True):
    id: int = Field(primary_key=True)
    conta_id: int = Field(foreign_key="conta.id")
    conta:Conta = Relationship()
    tipo: Tipos = Field(default=Tipos.ENTRADA)
    valor: float
    data: date

#criando a conexão com o banco

conexao = create_engine(sql_url, echo=True)

if __name__ == "__main__":
    model.metadata.create_all(conexao)

