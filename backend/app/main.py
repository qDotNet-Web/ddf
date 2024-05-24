from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .core.database import db
from .core.middleware import request_handler
from .router import lobby_router, player_router, question_router
from .core.utils import sio
from socketio import ASGIApp

app = FastAPI()

origins = [
    "https://derduemmstefliegt.online",
    "http://derduemmstefliegt.online",
    ]

app.mount("/ws", ASGIApp(socketio_server=sio))


@sio.on('message')
async def handle_message(sid, data):
    print("Socket ID: ", sid)
    print("Data received: ", data)

app.middleware("http")(request_handler)
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(lobby_router.router, prefix="/lobby")
app.include_router(player_router.router, prefix="/player")
app.include_router(question_router.router, prefix="/question")


@app.on_event("startup")
async def startup_event() -> None:
    await db.initialize()


@app.on_event("shutdown")
async def shutdown_event() -> None:
    db.close()

'''
Spielprinzip:

1. Es können aktuell bis zu 10 Spieler spielen
2. Jemand wählt seinen Namen aus und erstellt eine Lobby
3. Man kann mit diesem Code Leute einladen
4. Wenn diese Joinen müssen sie einen Namen eintragen
5. Wenn die Lobby erstellt wurde, kann der Lobbyersteller die folgenden Einstellungen vornehmen: 
    - Rundentimer (Standard 3 Minuten)
    - Lebenanzahl pro Spieler
6. Wenn alle Spieler drin sind, kann man die Lobby starten
7. Während der Timer noch läuft, werden den Teilnehmern nacheinander Fragen gestellt. Diese müssen sie eintragen. Am Ende des Timers müssen alle Spieler einen Spieler mit der dümmsten Antwort raus voten. Der verliert dann eines seiner Leben
8. Hat man alle Leben weg, kann man nicht mehr weiter spielen, nur noch zuschauen
'''
