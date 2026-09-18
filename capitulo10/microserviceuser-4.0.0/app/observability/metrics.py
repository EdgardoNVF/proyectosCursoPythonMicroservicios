from fastapi import FastAPI

from prometheus_client import Counter

from prometheus_fastapi_instrumentator import (
    Instrumentator
)


CACHE_HITS = Counter(
    "microservice_cache_hits_total",
    "Numero total de Cache Hits"
)


CACHE_MISSES = Counter(
    "microservice_cache_misses_total",
    "Numero total de Cache Misses"
)


CACHE_ERRORS = Counter(
    "microservice_cache_errors_total",
    "Numero total de errores al utilizar Redis",
    [
        "operation"
    ]
)


def setup_metrics(
    app: FastAPI
) -> None:

    Instrumentator().instrument(
        app
    ).expose(
        app,
        endpoint="/metrics",
        include_in_schema=False
    )
