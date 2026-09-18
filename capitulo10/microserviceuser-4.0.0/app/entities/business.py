#en este archivo se definen las entidad de negocio del microservicio
from dataclasses import dataclass

@dataclass
class User:
    name:str
    email:str
    address:str
    id:int|None=None