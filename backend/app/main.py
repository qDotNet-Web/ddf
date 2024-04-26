from fastapi import FastAPI
from .api.endpoints import game, user
from .core.database import db


app = FastAPI()

app.include_router(game.router)
app.include_router(user.router)


@app.on_event("startup")
async def startup_event():
    await db.initialize()


@app.on_event("shutdown")
async def shutdown_event():
    db.close()