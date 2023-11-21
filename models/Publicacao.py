from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Publicacao:
    id: int
    legenda: str
    publico: bool = False
    dataPublicacao: Optional[datetime] = None
    idAutor: int = 0    #autor se refere ao usuário que está fazendo a publicação
    nomeAutor: str = ""
    idMusica: int = 0
    nomeMusica: str = ""
    idArtista: int = 0
    nomeArtista: str = ""