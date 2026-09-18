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


#respositorio de postgress
class RepositoryPostgres(
    Repository[User, int]
):

    def __init__(
        self,
        datasource: Datasource
    ) -> None:

        self.__datasource = datasource


    def insert(
        self,
        entity: User
    ) -> bool:

        with self.__datasource.get_db() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    INSERT INTO users (
                        name,
                        email,
                        address
                    )
                    VALUES (
                        %s,
                        %s,
                        %s
                    )
                    RETURNING id
                    """,
                    (
                        entity.name,
                        entity.email,
                        entity.address
                    )
                )

                result = cursor.fetchone()

                if result is None:
                    return False

                entity.id = result[0]

        return True


    def list_all(
        self
    ) -> list[User]:

        with self.__datasource.get_db() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT
                        id,
                        name,
                        email,
                        address
                    FROM users
                    ORDER BY id
                    """
                )

                rows = cursor.fetchall()

        return [
            User(
                id=row[0],
                name=row[1],
                email=row[2],
                address=row[3]
            )
            for row in rows
        ]


    def update(
        self,
        entity: User
    ) -> bool:

        if entity.id is None:

            raise ValueError(
                "ID vacío"
            )

        with self.__datasource.get_db() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    UPDATE users
                    SET
                        name = %s,
                        email = %s,
                        address = %s
                    WHERE id = %s
                    """,
                    (
                        entity.name,
                        entity.email,
                        entity.address,
                        entity.id
                    )
                )

                return cursor.rowcount > 0


    def delete_by_id(
        self,
        entity_id: int
    ) -> bool:

        with self.__datasource.get_db() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    DELETE FROM users
                    WHERE id = %s
                    """,
                    (
                        entity_id,
                    )
                )

                return cursor.rowcount > 0


