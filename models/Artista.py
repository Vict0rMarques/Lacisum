from dataclasses import dataclass
from typing import Optional
from models.Usuario import Usuario

@dataclass
class Artista(Usuario):
    qtdeOuvintes: Optional[int] = ""