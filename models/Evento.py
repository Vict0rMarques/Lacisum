from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Evento:
    id: int
    nome: str
    descricao: str
    datahora: datetime
    cidade: str
    local: str
    idOrganizador: int
    foto: Optional[bytes] = b""
    idCategoria: int = 0
    nomeCategoria: str = ""