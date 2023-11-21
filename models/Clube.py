from dataclasses import dataclass
from typing import Optional

@dataclass
class Clube:
    id: int
    nome: str
    descricao: str
    tipo: int
    condicao: int
    privacidade: int
    qtdeMembros: int
    idadeMinima: int
    fotoPerfil: Optional[bytes] = b""
    fotoCapa: Optional[bytes] = b""
    idArtista: int = 0
    nomeArtista: str = ""
    idPropietario: int = 0
    nomePropietario: str = ""