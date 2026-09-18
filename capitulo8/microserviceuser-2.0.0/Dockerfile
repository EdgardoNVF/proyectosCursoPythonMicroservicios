FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /microservice

COPY requirements.txt .

RUN pip install \
    --no-cache-dir \
    --upgrade pip \
    && pip install \
    --no-cache-dir \
    -r requirements.txt

RUN groupadd \
    --system \
    --gid 10001 \
    appgroup \
    && useradd \
    --system \
    --uid 10001 \
    --gid 10001 \
    --create-home \
    --home-dir /home/appuser \
    appuser

COPY \
    --chown=10001:10001 \
    app \
    ./app


WORKDIR /microservice/app

USER 10001:10001

EXPOSE 8000

CMD ["python","-m","uvicorn","main:app","--host","0.0.0.0","--port","8000"]