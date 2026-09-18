import os
from daos.daos import RepositoryPostgres
from datasource.postgre_datasource import PostgresDatasource
from services.services import UserService


DATABASE_URL = os.getenv(
    "DATABASE_URL"
)

if DATABASE_URL is None:
    raise RuntimeError(
        "DATABASE_URL no está configurada"
    )

datasource = PostgresDatasource(
    database_url=DATABASE_URL
)

repository = RepositoryPostgres(
    datasource
)

service = UserService(
    repository
)


def get_user_service() -> UserService:
    return service