from dataclasses import dataclass
from typing import Optional

@dataclass
class Artista:
    idUsuario: int
    canal: Optional[str]= ""
    qtdeOuvintes: Optional[int] = ""