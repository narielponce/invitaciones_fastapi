from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi.staticfiles import StaticFiles
from .database import engine, Base
from . import models
from .routers import templates, clientes, invitaciones

# --- Absolute Path Configuration for Static Files ---
# Directory containing this main.py file
APP_DIR = os.path.dirname(os.path.abspath(__file__))
# Path to the 'backend' directory (one level up from 'app')
BACKEND_DIR = os.path.dirname(APP_DIR)
# Absolute path to the 'uploads' directory
UPLOADS_DIR = os.path.join(BACKEND_DIR, "uploads")

# Ensure the uploads directory exists
os.makedirs(UPLOADS_DIR, exist_ok=True)
# --- End of Configuration ---

app = FastAPI(
    title="API de Invitaciones Digitales",
    description="Backend para gestionar eventos y confirmaciones.",
    version="0.1.0"
)

# Configuración de CORS
origins = [
    "http://localhost:8081",
    "http://127.0.0.1:8081",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar el directorio de archivos estáticos con la ruta absoluta
# IMPORTANTE: Esto debe ir ANTES de incluir los routers para evitar conflictos de rutas.
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")

# Incluir los routers de la API
app.include_router(templates.router)
app.include_router(clientes.router)
app.include_router(invitaciones.router)

@app.get("/")
async def root():
    return {"message": "¡El backend de Invitaciones Digitales está funcionando!"}
