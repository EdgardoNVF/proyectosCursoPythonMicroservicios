from fastapi import FastAPI
from controller.controllers import router
import os
from observability.metrics import setup_metrics

app = FastAPI(
    title="Users API",
    version="4.0.0"
)

app.include_router(router)

#iniciar instrumentación de microservicio
setup_metrics(app)

@app.get("/health")
def health()-> dict[str,str]:
    return {"message": "API OK"}


@app.get("/instance")
def instance():
    return {
        "pod": os.getenv("HOSTNAME")
    }