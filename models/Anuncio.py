from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Anuncio:
    id: int
    titulo: str
    descricao: str
    preco: float
    condicao: str
    datahora: Optional[datetime] = None
    idAnunciante: int = 0
    nomeAnunciante: str = ""