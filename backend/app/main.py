from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import Base, engine
from app.routes.interactions import router as interaction_router
from app.routes.chat import router as chat_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(interaction_router, prefix="/api")
app.include_router(chat_router, prefix="/api")


@app.get("/")
def health():
    return {"status": "running"}