from dataclasses import dataclass

@dataclass
class Bloqueio:
    idBloqueado: int = 0 #bloqueado se refere ao usuário que está sendo bloqueado
    nomeBloqueado: str = "" 
    idBloqueador: int = 0    #bloqueador se refere ao usuário que está bloqueando