from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class CurtidaPublicacao:
    dataCurtida: Optional[datetime] = None
    idAutor: int = 0    #autor se refere ao usuário que está curtindo a publicação
    nomeAutor: str = ""
    IdPublicacao: int = 0