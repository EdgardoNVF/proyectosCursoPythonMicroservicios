import os
from daos.daos import RepositoryMemory
from datasource.datasource import DatasourceJson
from services.services import UserService

#nombre de archivo
DATA_FILE= os.getenv(
    "DATA_FILE", 
    "/data/users.json"
)
datasource =DatasourceJson(filename=DATA_FILE)
repository = RepositoryMemory(datasource)
service = UserService(repository)


def get_user_service() -> UserService:
    return service