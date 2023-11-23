from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Usuario:
    id: int
    nome: str
    email: str
    dataNascimento: datetime  
    senha: Optional[str] = ""
    admin: Optional[bool] = False
    token: Optional[str] = "" 
    biografia: Optional[str] = ""
    qtdeSeguidores: Optional[int] = None
    dataCadastro: Optional[datetime] = None
    artista: Optional[bool] = False
