from dataclasses import dataclass
from typing import Optional

@dataclass
class Musica:
    id: int
    nome: str
    aprovado: Optional[bool] = False
    idArtista: int = 0
    nomeArtista: str = ""
    idEstiloMusical: int = 0
    nomeEstiloMusical: str = ""