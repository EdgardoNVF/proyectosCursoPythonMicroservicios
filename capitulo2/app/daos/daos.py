'''
En este archivo se definen los métodos disponibles
en nuestro microservicios con la fuente datos
'''

from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from datasource.datasource import Datasource
from entities.business import User

T = TypeVar("T")
ID = TypeVar("ID")

class Repository(ABC, Generic[T, ID]):

    @abstractmethod
    def insert(self, entity: T) -> bool:
        ...

    @abstractmethod
    def list_all(self) -> list[T]:
        ...

    @abstractmethod
    def update(self, entity: T) -> bool:
        ...

    @abstractmethod
    def delete_by_id(self, entity_id: ID) -> bool:
        ...


class RepositoryMemory(Repository[User, int]):

    def __init__(
        self,
        datasource: Datasource[list[User]]
    ) -> None:
        self.__datasource = datasource

    def insert(self, entity: User) -> bool:
        database = self.__datasource.get_db()

        entity_id = max(
            (
                user.id
                for user in database
                if user.id is not None
            ),
            default=0
        ) + 1

        entity.id = entity_id
        database.append(entity)

        self.__datasource.save_db(database)
        return True

    def list_all(self) -> list[User]:
        return self.__datasource.get_db().copy()

    def update(self, entity: User) -> bool:
        if entity.id is None:
            raise ValueError("ID vacío")
        database=self.__datasource.get_db()
        for stored_user in self.__datasource.get_db():
            if stored_user.id == entity.id:
                stored_user.address = entity.address
                stored_user.email = entity.email
                stored_user.name = entity.name

                self.__datasource.save_db(database)
                return True

        return False

    def delete_by_id(self, entity_id: int) -> bool:
        database = self.__datasource.get_db()

        for stored_user in database:
            if stored_user.id == entity_id:
                database.remove(stored_user)

                self.__datasource.save_db(database)
                return True

        return False
