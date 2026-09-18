from redis import Redis


class RedisDatasource:

    def __init__(
        self,
        redis_url: str
    ) -> None:

        self.__client = Redis.from_url(
            redis_url,
            decode_responses=True,
            socket_connect_timeout=1,
            socket_timeout=1
        )


    def get_client(
        self
    ) -> Redis:

        return self.__client
