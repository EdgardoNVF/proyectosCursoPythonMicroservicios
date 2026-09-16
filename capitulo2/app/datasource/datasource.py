'''
Definiremos el contrato de Datasource
y sus diferentes implementaciones
'''
import json
from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from dataclasses import asdict
from pathlib import Path
from entities.business import User

T=TypeVar("T")
class Datasource(ABC, Generic[T]):
    @abstractmethod
    def get_db(self)->T:
        ...

    @abstractmethod
    def save_db(self, data: list):
        ...

    @abstractmethod
    def close_connection(self):
        ...


#implementación 1
class DatasourceJson(Datasource[list[User]]):

    def __init__(self, filename: str):
        self.__path = Path(filename)

        self.__path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.__path.exists():
            self.__path.write_text(
                "[]",
                encoding="utf-8"
            )

    def get_db(self) -> list[User]:

        content = self.__path.read_text(
            encoding="utf-8"
        )

        data = json.loads(content)

        return [
            User(**item)
            for item in data
        ]

    def save_db(
        self,
        data: list[User]
    ) -> None:

        serialized = [
            asdict(user)
            for user in data
        ]

        self.__path.write_text(
            json.dumps(
                serialized,
                indent=2,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )

    def close_connection(self):
        pass
