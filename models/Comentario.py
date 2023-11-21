from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Comentario:
    id: int
    comentario: str
    dataComentario: Optional[datetime] = None
    idAutor: int = 0    #autor se refere ao usuário que está fazendo o comentário
    nomeAutor: str = ""