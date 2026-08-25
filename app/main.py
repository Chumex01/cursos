from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app import models 
from app.config import settings

# --- CREACIÓN DE TABLAS EN LA BASE DE DATOS ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas exitosamente.")
    yield

# Inicializamos la aplicación FastAPI
app = FastAPI(title="Mi API con FastAPI", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Creamos nuestra primera ruta (endpoint) usando un decorador
@app.get("/")
def leer_raiz():
    return {"mensaje": "¡Hola, Mundo! Bienvenido a mi API con FastAPI"}