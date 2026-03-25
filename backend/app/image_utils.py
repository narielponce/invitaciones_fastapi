import os
import uuid
from io import BytesIO
from PIL import Image
from fastapi import UploadFile

# --- Absolute Path Configuration for Uploads ---
# Directory containing this image_utils.py file
APP_DIR = os.path.dirname(os.path.abspath(__file__))
# Path to the 'backend' directory (one level up from 'app')
BACKEND_DIR = os.path.dirname(APP_DIR)
# Absolute path to the 'uploads' directory
UPLOADS_DIR = os.path.join(BACKEND_DIR, "uploads")
# --- End of Configuration ---


MAX_SIZE = 800

def process_and_save_image(upload_file: UploadFile) -> str:
    """
    Recibe un UploadFile, redimensiona, convierte a webp y guarda.
    Devuelve el nombre del archivo guardado.
    """
    if not upload_file.content_type.startswith("image/"):
        raise ValueError("File is not a valid image.")

    try:
        # Generar un nombre de archivo único con extensión .webp
        filename = f"{uuid.uuid4()}.webp"
        save_path = os.path.join(UPLOADS_DIR, filename)

        # Leer el contenido del archivo subido
        content = upload_file.file.read()
        img = Image.open(BytesIO(content))
        
        # Convertir a RGB (por si viene con transparencia o en otros modos)
        if img.mode not in ('RGB', 'L'): # L es para escala de grises
            img = img.convert('RGB')

        # Redimensionar si supera el tamaño máximo
        if img.height > MAX_SIZE or img.width > MAX_SIZE:
            img.thumbnail((MAX_SIZE, MAX_SIZE))

        # Guardar en un buffer en memoria en formato WEBP
        buffer = BytesIO()
        img.save(buffer, format='WEBP', quality=85)
        buffer.seek(0)

        # Escribir el buffer al archivo en el disco
        with open(save_path, "wb") as f:
            f.write(buffer.read())

        return filename

    except Exception as e:
        print(f"Error procesando imagen: {e}")
        # En un caso real, podrías querer levantar una excepción HTTP aquí
        raise e
