from dataclasses import dataclass

@dataclass
class Seguidor:
    idSeguidor: int = 0 #seguidor se refere ao usuário que está seguindo
    nomeSeguidor: str = "" 
    idSeguido: int = 0    #seguido se refere ao usuário que está sendo seguido