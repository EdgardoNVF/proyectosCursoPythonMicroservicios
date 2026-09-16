from daos.daos import Repository
from entities.business import User

class UserService:
    def __init__(self,repository:Repository[User,int])->None:
        self.__repository=repository

    def insert(self, user:User)->bool:
        if not user.name.strip():
            raise ValueError("el nombre es obligatorio")

        if not self.__repository.insert(user):
            raise RuntimeError("no fue posible crear el usuario")
        return True

    def list_all(self)->list[User]:
        return self.__repository.list_all()

    def update(self, user: User) -> bool:
        if user.id is None:
            raise ValueError("El ID es obligatorio")

        if not self.__repository.update(user):
            raise ValueError("Usuario no encontrado")

        return True

    def delete(self, user_id: int) -> None:
        if not self.__repository.delete_by_id(user_id):
            raise ValueError("Usuario no encontrado")
