import psycopg
from typing import Any
from datasource.datasource import Datasource

class PostgresDatasource(Datasource[Any]):
    def __init__(
            self,
            database_url: str
    )->None:
        self.__database_url = database_url
    
    def get_db(self) ->Any:
        return psycopg.connect(self.__database_url)

    def save_db(self, data: list):
        raise NotImplementedError

    def close_connection(self):
        raise NotImplementedError

