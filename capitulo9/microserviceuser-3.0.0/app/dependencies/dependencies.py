import os

from daos.daos import RepositoryPostgres

from daos.cached_repository import (
    CachedUserRepository
)

from datasource.postgre_datasource import (
    PostgresDatasource
)

from datasource.redis_datasource import (
    RedisDatasource
)

from services.services import UserService


DATABASE_URL = os.getenv(
    "DATABASE_URL"
)


if DATABASE_URL is None:

    raise RuntimeError(
        "DATABASE_URL no está configurada"
    )


REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://redis:6379/0"
)


CACHE_TTL_SECONDS = int(
    os.getenv(
        "CACHE_TTL_SECONDS",
        "60"
    )
)


postgres_datasource = (
    PostgresDatasource(
        database_url=DATABASE_URL
    )
)


postgres_repository = (
    RepositoryPostgres(
        postgres_datasource
    )
)


redis_datasource = (
    RedisDatasource(
        redis_url=REDIS_URL
    )
)


repository = CachedUserRepository(

    repository=postgres_repository,

    cache=redis_datasource.get_client(),

    ttl_seconds=CACHE_TTL_SECONDS
)


service = UserService(
    repository
)


def get_user_service() -> UserService:

    return service
