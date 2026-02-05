from fastapi import FastAPI
from buildings.router import router as buildings_router


app = FastAPI(
    title="Система видеонаблюдения",
    version="0.1.0",
    root_path="/api"
)

app.include_router(buildings_router)
