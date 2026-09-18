from fastapi import FastAPI
from controller.controllers import router
import os

app = FastAPI(
    title="Users API",
    version="2.0.0"
)

app.include_router(router)

@app.get("/health")
def health()-> dict[str,str]:
    return {"message": "API OK"}


@app.get("/instance")
def instance():
    return {
        "pod": os.getenv("HOSTNAME")
    }