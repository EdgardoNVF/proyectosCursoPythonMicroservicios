import json
import logging

from dataclasses import asdict

from redis import Redis
from redis import RedisError

from daos.daos import Repository

from entities.business import User


logger = logging.getLogger(
    "uvicorn.error"
)


class CachedUserRepository(
    Repository[User, int]
):

    CACHE_KEY = (
        "microserviceuser:v1:users:all"
    )


    def __init__(
        self,
        repository: Repository[User, int],
        cache: Redis,
        ttl_seconds: int = 60
    ) -> None:

        self.__repository = repository

        self.__cache = cache

        self.__ttl_seconds = ttl_seconds


    def list_all(
        self
    ) -> list[User]:

        try:

            cached_value = self.__cache.get(
                self.CACHE_KEY
            )

            if cached_value is not None:

                logger.info(
                    "CACHE HIT key=%s",
                    self.CACHE_KEY
                )

                data = json.loads(
                    cached_value
                )

                return [
                    User(**item)
                    for item in data
                ]


            logger.info(
                "CACHE MISS key=%s",
                self.CACHE_KEY
            )


        except (
            RedisError,
            json.JSONDecodeError,
            TypeError
        ) as error:

            logger.warning(
                "CACHE ERROR GET key=%s error=%s",
                self.CACHE_KEY,
                error
            )


        users = (
            self.__repository.list_all()
        )


        try:

            value = json.dumps(
                [
                    asdict(user)
                    for user in users
                ]
            )


            self.__cache.set(
                self.CACHE_KEY,
                value,
                ex=self.__ttl_seconds
            )


            logger.info(
                "CACHE SET key=%s ttl=%s",
                self.CACHE_KEY,
                self.__ttl_seconds
            )


        except RedisError as error:

            logger.warning(
                "CACHE ERROR SET key=%s error=%s",
                self.CACHE_KEY,
                error
            )


        return users


    def insert(
        self,
        entity: User
    ) -> bool:

        result = self.__repository.insert(
            entity
        )

        if result:

            self.__invalidate_cache()

        return result


    def update(
        self,
        entity: User
    ) -> bool:

        result = self.__repository.update(
            entity
        )

        if result:

            self.__invalidate_cache()

        return result


    def delete_by_id(
        self,
        entity_id: int
    ) -> bool:

        result = (
            self.__repository.delete_by_id(
                entity_id
            )
        )

        if result:

            self.__invalidate_cache()

        return result


    def __invalidate_cache(
        self
    ) -> None:

        try:

            deleted = self.__cache.delete(
                self.CACHE_KEY
            )

            logger.info(
                "CACHE INVALIDATE key=%s deleted=%s",
                self.CACHE_KEY,
                deleted
            )


        except RedisError as error:

            logger.warning(
                "CACHE ERROR DELETE key=%s error=%s",
                self.CACHE_KEY,
                error
            )
